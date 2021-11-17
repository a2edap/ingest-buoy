import os
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt

from utils import IngestPipeline, format_time_xticks
from tsdat import DSUtil
from typing import Dict


class Pipeline(IngestPipeline):
    """--------------------------------------------------------------------------------
    EXAMPLE INGEST INGESTION PIPELINE

    This is an example ingest meant to demonstrate how one might set up an ingestion
    pipeline using this template repository. It should be deleted before this
    repository or any of its ingests are used in a production environment.

    --------------------------------------------------------------------------------"""

    def hook_customize_raw_datasets(
        self, raw_dataset_mapping: Dict[str, xr.Dataset]
    ) -> Dict[str, xr.Dataset]:
        return raw_dataset_mapping

    def hook_customize_dataset(
        self, dataset: xr.Dataset, raw_mapping: Dict[str, xr.Dataset]
    ) -> xr.Dataset:
        return dataset

    def hook_finalize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        return dataset

    def hook_generate_and_persist_plots(self, dataset: xr.Dataset):
        # Useful variables
        date = pd.to_datetime(dataset.time.data[0]).strftime("%d-%b-%Y")
        location = dataset.attrs["location_meaning"]

        # Set styling context
        style_file = os.path.join(os.path.dirname(__file__), "styling.mplstyle")
        with plt.style.context(style_file):

            # Make and save plot of example variable
            filename = DSUtil.get_plot_filename(dataset, "example_var", "png")
            with self.storage._tmp.get_temp_filepath(filename) as tmp_path:
                fig, ax = plt.subplots()
                dataset["example_var"].plot(ax=ax, x="time")
                fig.suptitle(f"Example Variable at {location} on {date}")
                format_time_xticks(ax)
                fig.savefig(tmp_path)
                self.storage.save(tmp_path)
                plt.close(fig)
