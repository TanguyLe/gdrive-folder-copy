from pathlib import Path
import logging
from typing import Optional

from googleapiclient.discovery import build

from gdfc.auth_utils import get_and_save_auth_token


class FolderNameError(Exception):
    pass


FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"
logger = logging.getLogger(__name__)


class GDriveClient:
    def __init__(self, auth_folder_path: Path):

        logger.info(f"Authentication with files in {auth_folder_path}.")
        self._service = build(
            serviceName='drive', version='v3', credentials=get_and_save_auth_token(auth_folder_path=auth_folder_path)
        )
        self._auth_folder_path = auth_folder_path
        logger.info("Authentication successful.")

    def _get_folder_id_by_name(self, folder_name: str):
        resp = self._service.files().list(
            q=f"name=\"{folder_name}\" and trashed=false", fields="files(id, name)"
        ).execute()

        resp_files = resp["files"]

        if len(resp_files) > 1:
            raise FolderNameError(
                f"Several folders exist with the name {folder_name}, "
                f"handling those is currently not implemented. You may want to also check the trash."
            )
        if not resp_files:
            raise FolderNameError(
                f"No folder exist with the name {folder_name}."
            )

        return resp_files[0]["id"]

    def _get_folder_children(self, folder_id: str):
        resp = self._service.files().list(q=f"\"{folder_id}\" in parents and trashed=false").execute()

        return resp["files"]

    def _copy_single_file(self, file_id: str, target_file_name: str, parent_target_folder_id: str = "root"):
        logger.info(f"Copying file \"{file_id}\" as \"{target_file_name}\" to \"{parent_target_folder_id}\"")
        body = {"parents": [{"kind": "drive#fileLink", "id": parent_target_folder_id}], 'name': target_file_name}
        self._service.files().copy(fileId=file_id, body=body).execute()

    def _create_folder(self, target_folder_name: str, parent_target_folder_id: str = "root"):
        logger.info(f"Create folder \"{target_folder_name}\" at \"{parent_target_folder_id}\"")

        body = {
            "parents": [{"kind": "drive#fileLink", "id": parent_target_folder_id}],
            'name': target_folder_name,
            "mimeType": FOLDER_MIME_TYPE
        }
        return self._service.files().create(body=body).execute()

    def _copy_folder(self, folder_id: str, target_folder_name: str, parent_target_folder_id: str = "root"):
        logger.info(f"Copying folder \"{folder_id}\" as \"{target_folder_name}\" to \"{parent_target_folder_id}\"")

        new_folder = self._create_folder(
            target_folder_name=target_folder_name, parent_target_folder_id=parent_target_folder_id
        )
        children = self._get_folder_children(folder_id=folder_id)

        for child in children:
            if child["mimeType"] == FOLDER_MIME_TYPE:
                self._copy_folder(
                    folder_id=child["id"], target_folder_name=child["name"], parent_target_folder_id=new_folder["id"]
                )
            else:
                self._copy_single_file(
                    file_id=child["id"], target_file_name=child["name"], parent_target_folder_id=new_folder["id"]
                )

    def copy_folder(self, folder_name: str, parent_target_folder_name: str, target_folder_name: Optional[str] = None):
        target_folder_name = target_folder_name if target_folder_name is not None else folder_name
        logger.info(
            f"Copying folder named \"{folder_name}\" as \"{target_folder_name}\" "
            f"to folder named \"{parent_target_folder_name}\""
        )

        source_folder_id = self._get_folder_id_by_name(folder_name=folder_name)
        target_folder_id = self._get_folder_id_by_name(folder_name=parent_target_folder_name)

        self._copy_folder(
            folder_id=source_folder_id, target_folder_name=target_folder_name, parent_target_folder_id=target_folder_id
        )
