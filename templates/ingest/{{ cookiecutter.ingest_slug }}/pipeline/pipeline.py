import os
import xarray as xr
import matplotlib.pyplot as plt

from typing import Dict
from utils import IngestPipeline


# TODO – Developer: Use hooks to add custom functionality to the pipeline including
# plots, as applicable. Remove any unused code.


class Pipeline(IngestPipeline):
    """--------------------------------------------------------------------------------
    {{ cookiecutter.ingest.upper() }} INGESTION PIPELINE

    {{ cookiecutter.description }}

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
        style_file = os.path.join(os.path.dirname(__file__), "styling.mplstyle")
        with plt.style.context(style_file):
            pass
