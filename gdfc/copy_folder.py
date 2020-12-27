from pathlib import Path
import logging

from gdfc.gdrive_client import GDriveClient

logger = logging.getLogger(__name__)


def copy_folder(
        source_folder_name: str, target_folder_parent_name: str, target_folder_name: str, auth_folder_path: Path
) -> None:
    logger.info(f"Copying \"{source_folder_name}\" as \"{target_folder_name}\" in \"{target_folder_parent_name}\".")

    client = GDriveClient(auth_folder_path=auth_folder_path)
    client.copy_folder(
        folder_name=source_folder_name,
        target_folder_name=target_folder_name,
        parent_target_folder_name=target_folder_parent_name
    )
