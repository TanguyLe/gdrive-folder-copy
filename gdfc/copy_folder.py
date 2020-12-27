from pathlib import Path
import logging

from googleapiclient.discovery import build

from gdfc.auth_utils import get_and_save_auth_token

logger = logging.getLogger(__name__)


def copy_folder(
        source_folder_name: str, target_folder_parent_name: str, target_folder_name: str, auth_folder_path: Path
) -> None:
    logger.info(f"Copying {source_folder_name} as {target_folder_name} in {target_folder_parent_name}.")

    logger.info(f"Authentication with files in {auth_folder_path}.")
    creds = get_and_save_auth_token(auth_folder_path=auth_folder_path)
    service = build('drive', 'v3', credentials=creds)
    logger.info("Authentication successful.")
