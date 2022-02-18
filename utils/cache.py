import pkgutil
import importlib
import logging

from tsdat.io import S3Path
from typing import AnyStr, Dict, List, Union
from .specification import IngestSpec

logger = logging.getLogger(__name__)


class PipelineCache:
    """----------------------------------------------------------------------------
    Utility class to discover and cache `A2ePipeline` classes and the configuration
    specifications needed to instatiate them later.

    ----------------------------------------------------------------------------"""

    def __init__(self, auto_discover: bool = False):
        self._modules: List[str] = list()
        self._cache: Dict["AnyStr@compile", IngestSpec] = dict()
        if auto_discover:
            self.discover_all()

    def discover_all(self, parent_module="ingest"):
        """----------------------------------------------------------------------------
        Discovers all ingests under the parent module and registers them for later use.


        Args:
            parent_module (str, optional): The module (relative to the "ingest-awaken"
            folder) under which individual ingests live. Defaults to "ingest".

        ----------------------------------------------------------------------------"""
        for ingest_module_info in pkgutil.iter_modules([parent_module]):
            self._modules.append(ingest_module_info.name)
            ingest_module_classname = f"ingest.{ingest_module_info.name}"
            ingest_module = importlib.import_module(ingest_module_classname)
            mappings: Dict["AnyStr@compile", IngestSpec] = ingest_module.mapping
            for regex, specification in mappings.items():
                self._register(regex, specification)
        logger.debug("Discovered ingest modules: %s", self._modules)

    def match_filepath(self, input_files: Union[List[S3Path], List[str]]) -> IngestSpec:
        """----------------------------------------------------------------------------
        Matches the provided files to a registered `A2ePipeline` and cached
        configuration parameters.

        Note that if multiple files are passed together, it is assummed that they must
        be co-processed in the same pipeline invocation. Only the first file in the
        list will be used for the matching.

        Args:
            input_files (Union[List[S3Path], List[str]]): A list of filepaths that the
            pipeline will later be run against. This will either be S3 paths if running
            in AWS mode or string paths if running in local mode.

        Returns:
            IngestSpec: The specifications needed to instantiate the appropriate
            `A2ePipeline` pipeline for the provided inputs.

        ----------------------------------------------------------------------------"""
        query_filepath = input_files[0].__str__()
        regex_key = self._match_key(query_filepath)
        return self._cache[regex_key]

    def _register(
        self,
        regex: "AnyStr@compile",
        specification: IngestSpec,
    ):
        """----------------------------------------------------------------------------
        Adds a compiled regex pattern to the internal cache. The regex helps to map
        files matching a specific pattern to a specific set of pipeline and storage
        configurations for a non-instantiated A2ePipeline class.

        See https://docs.python.org/3.8/howto/regex.html for more information on Python
        regexes.

        Args:
            regex (AnyStr): A compiled regex pattern which should match files to
            process. This is typically created by `re.compile(...)`.
            pipeline_cls (A2ePipeline): The `A2ePipeline` class to associate with the
            regex pattern. *Must not be an instance of a class*
            pipeline_config (str): The full path to the pipeline configuration file to
            instantiate the `A2ePipeline` with.
            storage_config (str): The full path to the storage configuration file to
            instantiate the `A2ePipeline` with.

        ----------------------------------------------------------------------------"""
        assert regex not in self._cache
        self._cache[regex] = specification

    def _match_key(self, filepath: str) -> "AnyStr@compile":
        """----------------------------------------------------------------------------
        Matches the provided filepath against the list of registered regex patterns. If
        and only if there is exactly one match this returns the regex pattern matching
        the filepath, as this is the key in the `PipelineCache._cache` dictionary.
        Raises an `AssertionError` if there is not exactly one match.

        Args:
            filepath (str): The filepath to match with a registered regex pattern.

        Returns:
            "AnyStr@compile": The (single) regex pattern that matches the filepath.

        ----------------------------------------------------------------------------"""
        matches: List[str] = [
            regex for regex in self._cache.keys() if regex.match(filepath)
        ]
        if len(matches) != 1:
            raise ValueError(
                f"Unexpected number of matches for file '{filepath}':\n"
                f"matches={matches}"
            )
        return matches[0]
