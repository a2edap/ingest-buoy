# This class dispatches the pipeline based on an input. It selects the appopriate
# method (Pipeline.run(...) vs Pipeline.run_plots(...)) based on mapping – if "plots"
# is part of the IngestSpec.name string then dispatch to _run_plots()

import logging
from tsdat.io import S3Path
from typing import List, Union
from .cache import PipelineCache


logger = logging.getLogger(__name__)


class PipelineDispatcher:
    def __init__(self, auto_discover: bool = False):
        self._cache = PipelineCache(auto_discover=auto_discover)

    def dispatch(self, input_files: Union[List[S3Path], List[str]]) -> bool:
        """----------------------------------------------------------------------------
        Instantiates the appropriate `A2ePipeline` for the provided input files and
        calls either the `A2ePipeline.run()` or `A2ePipeline.run_plots()` method
        according to the ingest's `mapping` specifications.

        Args:
            input_files (Union[List[S3Path], List[str]]): A list of filepaths that the
            pipeline will later be run against. This will either be S3 paths if running
            in AWS mode or string paths if running in local mode.

        Returns:
            bool: True if the Pipeline and method were dispatched and ran without
            error, False otherwise.

        ----------------------------------------------------------------------------"""
        if not isinstance(input_files, List):
            input_files = [input_files]

        status = True

        # TODO: Catch possible exceptions:
        # AssertionError – no regex match, or too many matches`
        # FileNotFoundError – bad config file path or data file path
        # DefinitionError – a config file not defined correctly.
        # QCError – pipeline failed because of poor data quality – manual intervention
        # BaseException – any other error: catch, report, and carry on.
        try:
            specification = self._cache.match_filepath(input_files)
            pipeline = specification.instantiate()
            if "plot" in specification.name:
                pipeline.run_plots(input_files)
            else:
                pipeline.run(input_files)
        except BaseException:
            logger.exception("Pipeline failed on input files: %s", input_files)
            status = False

        return status
