from pydantic import BaseModel, Extra
import xarray as xr
import pandas as pd
import numpy as np
from tsdat import DataReader


class BuoyReader(DataReader):
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

    def read(self, input_key) -> xr.Dataset:
        df: pd.DataFrame = pd.read_csv(input_key, index_col=0)  # type: ignore
        ds = xr.Dataset.from_dataframe(df)

        if "Vel1 (mm/s)" in ds.variables:

            def has_vel_and_dir(index: int) -> bool:
                has_vel = f"Vel{index+1} (mm/s)" in ds.variables
                has_dir = f"Dir{index+1} (deg)" in ds.variables
                return has_vel and has_dir

            # Calculate depths and collect data vars
            i = 0
            depth, vel_data, dir_data = [], [], []
            # Location of first bin from ADCP
            first_bin = (
                df["HeadDepth"][0] + df["BlankingDistance"][0] + df["BinSpacing"][0]
            )  # .85 m instrument depth + 0.5 m blank + 4 m bin size
            # Create 2D matrix of ADCP data
            while has_vel_and_dir(i):
                depth.append(first_bin + 4 * i)
                vel_data.append(ds[f"Vel{i+1} (mm/s)"].data)
                dir_data.append(ds[f"Dir{i+1} (deg)"].data)
                i += 1

            depth = np.array(depth)  # type: ignore
            vel_data = np.array(vel_data)  # type: ignore
            dir_data = np.array(dir_data)  # type: ignore

            # Make depth coordinate variables
            ds["depth"] = xr.DataArray(data=depth, dims=["depth"])
            ds = ds.set_coords("depth")

            # Add current velocity and direction data to dataset
            ds["current_speed"] = xr.DataArray(data=vel_data, dims=["depth", "time"])
            ds["current_direction"] = xr.DataArray(
                data=dir_data, dims=["depth", "time"]
            )

        # Hack if currents file is missing
        if "depth" not in ds:
            ds["depth"] = xr.DataArray(
                [0, 1, 2],
                dims=["depth"],
                attrs={"description": "Placeholder for missing ADCP data"},
            )

        return ds
