import typer

from typing import List
from pathlib import Path
from enum import Enum
from utils import (
    logger,
    PipelineDispatcher,
    set_dev_env,
    set_prod_env,
)


# TODO: Examine logging more closely –  can this be improved?


app = typer.Typer()


class Mode(str, Enum):
    aws = "aws"
    local = "local"


@app.command()
def run_pipeline(
    files: List[Path] = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="Path(s) to the file(s) to process",
    ),
    mode: Mode = typer.Option(Mode.local, help="The processing mode to use."),
):
    """
    Main entry point to the ingest controller. This script takes a path to an input
    file, automatically determines which ingest(s) to use, and runs those ingests
    on the provided input data.

    Args:
        input_file (str): The path to the input file to process.
        mode (str, optional): The processing mode used.

    """

    logger.debug(f"Using [{mode.value}] mode to run the follow file:\n{files}")
    if mode.value == Mode.local:
        set_dev_env()
    elif mode == Mode.aws:
        set_prod_env()

    logger.info(f"Found input files: {files}")

    dispatcher = PipelineDispatcher(auto_discover=True)

    logger.debug(f"Discovered ingest modules: \n{dispatcher._cache._modules}")

    success = dispatcher.dispatch(files)

    logger.info(f"Pipeline status: {'success' if success else 'failure'}")


if __name__ == "__main__":
    typer.run(run_pipeline)
