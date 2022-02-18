import typer
import logging

from typing import List
from pathlib import Path
from enum import Enum
from utils import PipelineDispatcher, set_env


# TODO: Examine logging more closely –  can this be improved?
logger = logging.getLogger(__name__)

app = typer.Typer(add_completion=False)


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
    clump: bool = typer.Option(
        False,
        help="Clump all the files together to be run by a single ingest. This typically"
        " results in one output data file being produced. Omit this option to run files"
        " independently and generally produce one output data file for each input file.",
    ),
):
    """Main entry point to the ingest controller. This script takes a path to an input
    file, automatically determines which ingest(s) to use, and runs those ingests on the
    provided input data."""
    set_env()

    # Downstream code expects a list of strings
    files: List[str] = [str(file) for file in files]
    logger.debug(f"Found input files: {files}")

    if clump:
        files = [files]

    # Run the pipeline on the input files
    dispatcher = PipelineDispatcher(auto_discover=True)
    logger.debug(f"Discovered ingest modules: \n{dispatcher._cache._modules}")

    successes = 0
    failures = 0
    for file in files:
        success = dispatcher.dispatch(file)  # Automatically catches and logs exceptions
        if success:
            logger.info("Successfully processed input: '%s'", file)
            successes += 1
        else:
            logger.warning("Failed to process input: '%s'", file)
            failures += 1

    logger.info("Done! (%d succeeded, %d failed)", successes, failures)


if __name__ == "__main__":
    app()
