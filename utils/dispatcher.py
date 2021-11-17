# This class dispatches the pipeline based on an input. It selects the appopriate
# method (Pipeline.run(...) vs Pipeline.run_plots(...)) based on mapping – if "plots"
# is part of the IngestSpec.name string then dispatch to _run_plots()

from tsdat.io import S3Path
from typing import List, Union
from .cache import PipelineCache


class PipelineDispatcher:
    def __init__(self, auto_discover: bool = False):
        self._cache = PipelineCache(auto_discover=auto_discover)

    def dispatch(self, input_files: Union[List[S3Path], List[str]]) -> bool:
        """----------------------------------------------------------------------------
        Instantiates the appropriate `IngestPipeline` for the provided input files and
        calls either the `IngestPipeline.run()` or `IngestPipeline.run_plots()` method
        according to the ingest's `mapping` specifications.

        Args:
            input_files (Union[List[S3Path], List[str]]): A list of filepaths that the
            pipeline will later be run against. This will either be S3 paths if running
            in AWS mode or string paths if running in local mode.

        Returns:
            bool: True if the Pipeline and method were dispatched and ran without
            error, False otherwise.

        ----------------------------------------------------------------------------"""

        specification = self._cache.match_filepath(input_files)

        if "plot" in specification.name:
            return self._run_plots(input_files)

        return self._run_pipeline(input_files)

    def _run_pipeline(self, input_files: Union[List[S3Path], List[str]]) -> bool:

        # TODO: Catch possible exceptions:
        # AssertionError – no regex match, or too many matches`
        # FileNotFoundError – bad config file path or data file path
        # DefinitionError – a config file not defined correctly.
        # QCError – pipeline failed because of poor data quality – manual intervention
        # BaseException – any other error: catch, report, and carry on.
        try:
            specification = self._cache.match_filepath(input_files)
            pipeline = specification.instantiate()
            pipeline.run(input_files)
        except BaseException:
            return False

        return True

    def _run_plots(self, input_files: Union[List[S3Path], List[str]]) -> bool:

        # TODO: Catch possible exceptions:
        # AssertionError – no regex match, or too many matches
        # FileNotFoundError – bad config file path or data file path
        # DefinitionError – a config file not defined correctly.
        # QCError – pipeline failed because of poor data quality – manual intervention
        # BaseException – any other error: catch, report, and carry on.
        try:
            specification = self._cache.match_filepath(input_files)
            pipeline = specification.instantiate()
            pipeline.run_plots(input_files)
        except BaseException:
            return False

        return True
