from __future__ import annotations

import logging
import os
import uuid

from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urlparse

import requests
import smart_open

from backports.cached_property import cached_property
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed
from typing_extensions import Protocol

from gretel_client.config import ClientConfig, DEFAULT_GRETEL_ARTIFACT_ENDPOINT
from gretel_client.dataframe import _DataFrameT
from gretel_client.projects.common import f
from gretel_client.rest.api.projects_api import ProjectsApi
from gretel_client.rest.exceptions import NotFoundException
from gretel_client.rest.model.artifact import Artifact


class ArtifactsException(Exception):
    pass


# These exceptions are used for control flow with retries in get_artifact_manifest.
# They are NOT intended to bubble up out of this module.
class ManifestNotFoundException(Exception):
    pass


class ManifestPendingException(Exception):
    def __init__(self, msg: Optional[str] = None, manifest: dict = {}):
        # Piggyback the pending manifest onto the exception.  If we give up, we still want to pass it back as a normal return value.
        self.manifest = manifest
        super().__init__(msg)


class _Project(Protocol):
    @property
    def project_id(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def projects_api(self) -> ProjectsApi:
        ...

    @property
    def client_config(self) -> ClientConfig:
        ...


def cloud_handler(project: _Project) -> CloudArtifactsHandler:
    return CloudArtifactsHandler(
        projects_api=project.projects_api,
        project_id=project.project_id,
        project_name=project.name,
    )


def hybrid_handler(project: _Project) -> HybridArtifactsHandler:
    endpoint = project.client_config.artifact_endpoint

    if endpoint == DEFAULT_GRETEL_ARTIFACT_ENDPOINT:
        raise ArtifactsException(
            "Cannot manage artifacts with hybrid strategy without custom artifact endpoint."
        )

    return HybridArtifactsHandler(endpoint=endpoint, project_id=project.project_id)


class ArtifactsHandler(Protocol):
    def upload_project_artifact(
        self,
        artifact_path: Union[Path, str, _DataFrameT],
    ) -> str:
        ...

    def delete_project_artifact(self, key: str) -> None:
        ...

    def list_project_artifacts(self) -> List[dict]:
        ...

    def get_project_artifact_link(self, key: str) -> str:
        ...

    def get_project_artifact_manifest(
        self,
        key: str,
        retry_on_not_found: bool = True,
        retry_on_pending: bool = True,
    ) -> Dict[str, Any]:
        ...

    def get_model_artifact_link(self, model_id: str, artifact_type: str) -> str:
        ...

    def get_record_handler_artifact_link(
        self,
        model_id: str,
        record_handler_id: str,
        artifact_type: str,
    ) -> str:
        ...

    def download(
        self,
        download_link: str,
        output_path: Path,
        artifact_type: str,
        log: logging.Logger,
    ) -> None:
        ...


class CloudArtifactsHandler:
    def __init__(self, projects_api: ProjectsApi, project_id: str, project_name: str):
        self.projects_api = projects_api
        self.project_id = project_id
        self.project_name = project_name

    def upload_project_artifact(
        self,
        artifact_path: Union[Path, str, _DataFrameT],
    ) -> str:
        if self._does_not_require_upload(artifact_path):
            return artifact_path

        artifact_path, file_name = _get_artifact_path_and_file_name(artifact_path)
        with smart_open.open(artifact_path, "rb", ignore_ext=True) as src:
            art_resp = self.projects_api.create_artifact(
                project_id=self.project_name, artifact=Artifact(filename=file_name)
            )
            artifact_key = art_resp[f.DATA][f.KEY]
            url = art_resp[f.DATA][f.URL]
            upload_resp = requests.put(url, data=src)
            upload_resp.raise_for_status()
            return artifact_key

    def _does_not_require_upload(
        self, artifact_path: Union[Path, str, _DataFrameT]
    ) -> bool:
        return isinstance(artifact_path, str) and artifact_path.startswith("gretel_")

    def delete_project_artifact(self, key: str) -> None:
        return self.projects_api.delete_artifact(project_id=self.project_name, key=key)

    def list_project_artifacts(self) -> List[dict]:
        return (
            self.projects_api.get_artifacts(project_id=self.project_name)
            .get(f.DATA)
            .get(f.ARTIFACTS)
        )

    def get_project_artifact_link(self, key: str) -> str:
        resp = self.projects_api.download_artifact(
            project_id=self.project_name, key=key
        )
        return resp[f.DATA][f.DATA][f.URL]

    # The server side API will return manifests with PENDING status if artifact processing has not completed
    # or it will return a 404 (not found) if you immediately request the artifact before processing has even started.
    # This is correct but not convenient.  To keep every end user from writing their own retry logic, we add some here.
    @retry(
        wait=wait_fixed(2),
        stop=stop_after_attempt(15),
        retry=retry_if_exception_type(ManifestPendingException),
        # Instead of throwing an exception, return the pending manifest.
        retry_error_callback=lambda retry_state: retry_state.outcome.exception().manifest,
    )
    @retry(
        wait=wait_fixed(3),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type(ManifestNotFoundException),
        # Instead of throwing an exception, return None.  Given that we waited for a short grace period to let the artifact become PENDING,
        # if we are still getting 404's the key probably does not actually exist.
        retry_error_callback=lambda retry_state: None,
    )
    def get_project_artifact_manifest(
        self,
        key: str,
        retry_on_not_found: bool = True,
        retry_on_pending: bool = True,
    ) -> Dict[str, Any]:
        resp = None
        try:
            resp = self.projects_api.get_artifact_manifest(
                project_id=self.project_name, key=key
            )
        except NotFoundException:
            raise ManifestNotFoundException()
        if retry_on_not_found and resp is None:
            raise ManifestNotFoundException()
        if retry_on_pending and resp is not None and resp.get("status") == "pending":
            raise ManifestPendingException(manifest=resp)
        return resp

    def get_model_artifact_link(self, model_id: str, artifact_type: str) -> str:
        art_resp = self.projects_api.get_model_artifact(
            project_id=self.project_name, model_id=model_id, type=artifact_type
        )
        return art_resp[f.DATA][f.URL]

    def get_record_handler_artifact_link(
        self,
        model_id: str,
        record_handler_id: str,
        artifact_type: str,
    ) -> str:
        resp = self.projects_api.get_record_handler_artifact(
            project_id=self.project_name,
            model_id=model_id,
            record_handler_id=record_handler_id,
            type=artifact_type,
        )
        return resp[f.DATA][f.URL]

    def download(
        self,
        download_link: str,
        output_path: Path,
        artifact_type: str,
        log: logging.Logger,
    ) -> None:
        artifact_response = requests.get(download_link)
        try:
            artifact_response.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            log.error(
                f"\tCould not download {artifact_type}. You might retry this request.",
                ex=ex,
            )
            return None

        artifact_output_path = output_path / Path(urlparse(download_link).path).name
        with open(artifact_output_path, "wb+") as out:
            log.info(f"\tWriting {artifact_type} to {artifact_output_path}")
            out.write(artifact_response.content)


class HybridArtifactsHandler:
    def __init__(self, endpoint: str, project_id: str):
        self.endpoint = endpoint
        self.project_id = project_id

    @cached_property
    def data_sources_dir(self) -> str:
        return f"{self.endpoint}/sources/{self.project_id}"

    def upload_project_artifact(
        self,
        artifact_path: Union[Path, str, _DataFrameT],
    ) -> str:
        if self._does_not_require_upload(artifact_path):
            return artifact_path

        artifact_path, file_name = _get_artifact_path_and_file_name(artifact_path)
        data_source_file_name = f"gretel_{uuid.uuid4().hex}_{file_name}"
        target_out = f"{self.data_sources_dir}/{data_source_file_name}"

        with smart_open.open(
            artifact_path, "rb", ignore_ext=True
        ) as in_stream, smart_open.open(target_out, "wb") as out_stream:
            out_stream.write(in_stream.read())

        return target_out

    def _does_not_require_upload(
        self, artifact_path: Union[Path, str, _DataFrameT]
    ) -> bool:
        return (
            isinstance(artifact_path, (str, Path))
            and not Path(artifact_path).expanduser().exists()
        )

    def delete_project_artifact(self, key: str) -> None:
        raise ArtifactsException("Cannot delete hybrid artifacts")

    def list_project_artifacts(self) -> List[dict]:
        raise ArtifactsException("Cannot list hybrid artifacts")

    def get_project_artifact_link(self, key: str) -> str:
        return f"{self.endpoint}/{self.project_id}/{key}"

    def get_project_artifact_manifest(
        self,
        key: str,
        retry_on_not_found: bool = True,
        retry_on_pending: bool = True,
    ) -> Dict[str, Any]:
        raise ArtifactsException("Artifact manifests do not exist for hybrid artifacts")

    def get_model_artifact_link(self, model_id: str, artifact_type: str) -> str:
        filename = ARTIFACT_FILENAMES.get(artifact_type)
        if filename is None:
            raise ArtifactsException(f"Unrecognized artifact type: `{artifact_type}`")

        return f"{self.endpoint}/{self.project_id}/model/{model_id}/{filename}"

    def get_record_handler_artifact_link(
        self,
        model_id: str,
        record_handler_id: str,
        artifact_type: str,
    ) -> str:
        filename = ARTIFACT_FILENAMES.get(artifact_type)
        if filename is None:
            raise ArtifactsException(f"Unrecognized artifact type: `{artifact_type}`")

        return f"{self.endpoint}/{self.project_id}/run/{record_handler_id}/{filename}"

    def download(
        self,
        download_link: str,
        output_path: Path,
        artifact_type: str,
        log: logging.Logger,
    ) -> None:
        target_out = output_path / Path(urlparse(download_link).path).name
        try:
            with smart_open.open(
                download_link, "rb", ignore_ext=True
            ) as in_stream, smart_open.open(target_out, "wb") as out_stream:
                out_stream.write(in_stream.read())
        except OSError:
            log.warning(
                f"Could not download {artifact_type} from `{download_link}`. The file may not exist, or you may not have access to it."
            )
            return None


def _get_artifact_path_and_file_name(
    artifact_path: Union[Path, str, _DataFrameT]
) -> Tuple[str, str]:
    if isinstance(artifact_path, _DataFrameT):
        artifact_path = BytesIO(artifact_path.to_csv(index=False).encode("utf-8"))
        file_name = f"dataframe-{uuid.uuid4()}.csv"
    else:
        if isinstance(artifact_path, Path):
            artifact_path = str(artifact_path)
        file_name = Path(urlparse(artifact_path).path).name

    return artifact_path, file_name


ARTIFACT_FILENAMES = {
    # Model artifacts
    "model": "model.tar.gz",
    "report": "report.html.gz",
    "report_json": "report_json.json.gz",
    "model_logs": "logs.json.gz",
    "data_preview": "data_preview.gz",
    "classification_report": "classification_report.html.gz",
    "classification_report_json": "classification_report_json.json.gz",
    "regression_report": "regression_report.html.gz",
    "regression_report_json": "regression_report_json.json.gz",
    # Record handler artifacts
    "run_report_json": "run_report_json.json.gz",
    "data": "data.gz",
    "run_logs": "logs.json.gz",
    "output_files": "output_files.tar.gz",
}
