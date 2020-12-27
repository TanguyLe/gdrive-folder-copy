import typer

app = typer.Typer()


@app.command()
def copy(
    source_folder: str,
    target_folder: str,
):
    raise NotImplementedError("copy command is not implemented yet.")


if __name__ == "__main__":
    app()
