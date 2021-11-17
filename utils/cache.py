import pkgutil
import importlib

from tsdat.io import S3Path
from typing import AnyStr, Dict, List, Union
from .specification import IngestSpec


class PipelineCache:
    """----------------------------------------------------------------------------
    Utility class to discover and cache `IngestPipeline` classes and the
    configuration specifications needed to instatiate them later.

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
            parent_module (str, optional): The module (relative to the repository root
            folder) under which individual ingests live. Defaults to "ingest".

        ----------------------------------------------------------------------------"""
        for ingest_module_info in pkgutil.iter_modules([parent_module]):
            self._modules.append(ingest_module_info.name)
            ingest_module_classname = f"ingest.{ingest_module_info.name}"
            ingest_module = importlib.import_module(ingest_module_classname)
            mappings: Dict["AnyStr@compile", IngestSpec] = ingest_module.mapping
            for regex, specification in mappings.items():
                self._register(regex, specification)

    def match_filepath(self, input_files: Union[List[S3Path], List[str]]) -> IngestSpec:
        """----------------------------------------------------------------------------
        Matches the provided files to a registered `IngestPipeline` and cached
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
            `IngestPipeline` pipeline for the provided inputs.

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
        configurations for a non-instantiated IngestPipeline class.

        See https://docs.python.org/3.8/howto/regex.html for more information on Python
        regexes.

        Args:
            regex (AnyStr): A compiled regex pattern which should match files to
            process. This is typically created by `re.compile(...)`.
            pipeline_cls (IngestPipeline): The `IngestPipeline` class to associate with
            the regex pattern. *Must not be an instance of a class*.
            pipeline_config (str): The full path to the pipeline configuration file to
            instantiate the `IngestPipeline` with.
            storage_config (str): The full path to the storage configuration file to
            instantiate the `IngestPipeline` with.

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
        # TODO: Probably helpful to distinguish 0 matches from >1 matches
        assert len(matches) == 1
        return matches[0]
