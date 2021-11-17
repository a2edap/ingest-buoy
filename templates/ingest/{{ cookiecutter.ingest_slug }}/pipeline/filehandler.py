import tsdat
import xarray as xr


# TODO – Developer: Write your FileHandler and add documentation
class CustomFileHandler(tsdat.AbstractFileHandler):
    """--------------------------------------------------------------------------------
    Custom file handler for reading <some data type> files from a <instrument name>
    for the A2E AWAKEN effort.

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
        return xr.Dataset()
