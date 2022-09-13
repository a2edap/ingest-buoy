from typing import Dict, Union
from pydantic import BaseModel, Extra
import xarray as xr
import pandas as pd
import numpy as np
import lzma

from tsdat import DataReader


class STADataReader(DataReader):
    """---------------------------------------------------------------------------------
    Custom DataReader that can be used to read data from a specific format.

    Built-in implementations of data readers can be found in the
    [tsdat.io.readers](https://tsdat.readthedocs.io/en/latest/autoapi/tsdat/io/readers)
    module.

    ---------------------------------------------------------------------------------"""

    class Parameters(BaseModel, extra=Extra.forbid):
        """If your CustomDataReader should take any additional arguments from the
        retriever configuration file, then those should be specified here.

        e.g.,:
        custom_parameter: float = 5.0

        """

    parameters: Parameters = Parameters()
    """Extra parameters that can be set via the retrieval configuration file. If you opt
    to not use any configuration parameters then please remove the code above."""

    def read(self, filename: str) -> Union[xr.Dataset, Dict[str, xr.Dataset]]:
        """----------------------------------------------------------------------------
        Method to read data in a custom format and convert it into an xarray Dataset.

        Args:
            filename (str): The path to the file to read in.

        Returns:
            xr.Dataset: An xr.Dataset object
        ----------------------------------------------------------------------------"""
        lzma_file = lzma.open(
            filename,
            encoding="cp1252",  # Default encoding for Windows devices
            mode="rt",
        )
        df = pd.read_csv(lzma_file, header=41, index_col=False, sep="\t",)
        dataset = df.to_xarray()

        # Add height variable
        dataset["height"] = xr.DataArray(
            data=[40, 60, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240], dims="height"
        )

        # Compress row of variables in input into variables dimensioned by time and height
        if ".sta" in filename:
            raw_categories = [
                "Wind Speed (m/s)",
                "Wind Speed Dispersion (m/s)",
                "Wind Speed min (m/s)",
                "Wind Speed max (m/s)",
                "Wind Direction (°)",
                "Z-wind (m/s)",
                "Z-wind Dispersion (m/s)",
                "CNR (dB)",
                "Dopp Spect Broad (m/s)",
                "Data Availability (%)",
            ]
            output_var_names = [
                "wind_speed",
                "horizontal_dispersion",
                "min_wind_speed",
                "max_wind_speed",
                "wind_direction",
                "vertical_wind_speed",
                "vertical_dispersion",
                "carrier_noise_ratio",
                "doppler_spectral_broadening",
                "data_availability",
            ]
            heights = dataset.height.data
            for category, output_name in zip(raw_categories, output_var_names):
                var_names = [f"{height}m {category}" for height in heights]
                var_data = [dataset[name].data for name in var_names]
                dataset = dataset.drop_vars(var_names)
                var_data = np.array(var_data).transpose()  # type: ignore
                dataset[output_name] = xr.DataArray(var_data, dims=["index", "height"])

        return dataset
