from pathlib import Path
from typing import Optional

import typer

from gdfc.copy_folder import copy_folder
from gdfc.log_utils import log_setup

app = typer.Typer()


@app.command()
@log_setup
def copy(
    source_folder_name: str,
    target_folder_parent_name: str = "root",
    target_folder_name: Optional[str] = None,
    auth_folder_path: Path = typer.Option(
        Path.cwd(),
        "--auth-folder-path",
        "-afp",
        exists=True,
        file_okay=True,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=True,
        help="Path where to get the token file and/or the credentials file. Default is the current directory.",
    )
):
    target_folder_name = source_folder_name if target_folder_name is None else target_folder_name
    copy_folder(
        source_folder_name=source_folder_name,
        target_folder_parent_name=target_folder_parent_name,
        target_folder_name=target_folder_name,
        auth_folder_path=auth_folder_path
    )


if __name__ == "__main__":
    app()
