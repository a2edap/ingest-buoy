import os
from .pipeline import IngestPipeline


class IngestSpec:
    """----------------------------------------------------------------------------
    Class to group the object and specifications needed to create an IngestPipeline
    instance that will be used to ingest data.

    ----------------------------------------------------------------------------"""

    def __init__(
        self,
        pipeline: IngestPipeline,
        pipeline_config: str,
        storage_config: str,
        name: str,
    ) -> None:
        """----------------------------------------------------------------------------
        Instantiates an IngestSpec class.

        Args:
            pipeline (IngestPipeline): A child class derived from the `IngestPipeline`
            parent class.
            pipeline_config (str): The path to the pipeline config file.
            storage_config (str): The path to the storage config file.
            name (str): The name of the ingest. This should be the name of the folder
            under which the ingest resides, though it will only be used for labelling
            purposes.

        ----------------------------------------------------------------------------"""
        assert issubclass(pipeline, IngestPipeline)
        assert os.path.isfile(pipeline_config)
        assert os.path.isfile(storage_config)

        self.pipeline = pipeline
        self.pipeline_config = pipeline_config
        self.storage_config = storage_config
        self.name = name

    def instantiate(self) -> IngestPipeline:
        """----------------------------------------------------------------------------
        Instantiates the pipeline using the previously-provided specifications.

        Returns:
            IngestPipeline: An instance of the provided pipeline class.

        ----------------------------------------------------------------------------"""
        return self.pipeline(self.pipeline_config, self.storage_config)
