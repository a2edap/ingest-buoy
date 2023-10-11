"""-------------------------------------------------------------------------------------
This module contains custom DataConverter classes that can be used when retrieving input
data from raw data files to convert data values to the format required by the output
dataset.yaml definition.

-------------------------------------------------------------------------------------"""

from typing import Any

import xarray as xr
from pydantic import BaseModel, Extra

from utils.a2e_tsdat.config.dataset import DatasetConfig
from utils.a2e_tsdat.io.base import DataConverter


# DEVELOPER: Implement your custom DataConverter, giving it a better name and
# documentation as you do so.
class CustomDataConverter(DataConverter):
    """---------------------------------------------------------------------------------
    Custom DataConverter that can be used to preprocess input datasets and convert them
    into a suitable format for downstream processing.

    Built-in examples of DataConverters include the UnitsConverter to convert units
    (e.g., degF -> degC) and the StringToDatetime converter to convert time variables
    encoded as strings into np.datetime64 objects.

    ---------------------------------------------------------------------------------"""

    class Parameters(BaseModel, extra=Extra.forbid):
        """If your CustomConverter should take any additional arguments from the
        retriever configuration file, then those should be specified here.

        e.g.,:
        custom_parameter: float = 5.0

        """

    parameters: Parameters = Parameters()
    """Extra parameters that can be set via the retrieval configuration file. If you opt
    to not use any configuration parameters then please remove the code above."""

    def convert(
        self,
        dataset: xr.Dataset,
        dataset_config: DatasetConfig,
        variable_name: str,
        **kwargs: Any,
    ) -> xr.Dataset:
        # Add your data conversion logic here
        raise NotImplementedError
        return dataset
