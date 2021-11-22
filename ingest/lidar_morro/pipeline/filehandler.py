import lzma
import tsdat
import pandas as pd
import xarray as xr


class StaFileHandler(tsdat.AbstractFileHandler):
    """--------------------------------------------------------------------------------
    Custom file handler for reading AXYS custom files from a Lidar instrument.

    See https://tsdat.readthedocs.io/en/latest/autoapi/tsdat/io/index.html for more
    examples of FileHandler implementations.

    --------------------------------------------------------------------------------"""

    def read(self, filename: str, **kwargs) -> xr.Dataset:
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
        df = pd.read_csv(
            lzma_file,
            header=41,
            index_col=False,
            sep="\t",
        )
        return df.to_xarray()
