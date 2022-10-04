import xarray as xr

import matplotlib.pyplot as plt
from tsdat import IngestPipeline, get_start_date_and_time_str, get_filename

from utils import format_time_xticks


class Imu(IngestPipeline):
    """--------------------------------------------------------------------------------
    IMU INGEST INGESTION PIPELINE

    Ingest of IMU data from an AXYS Technologies buoy stationed in Morro Bay, CA.

    --------------------------------------------------------------------------------"""

    def hook_customize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # Use this hook to modify the dataset before qc is applied
        return dataset

    def hook_finalize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # Use this hook to modify the dataset after qc is applied
        # but before it gets saved to the storage area
        return dataset

    def hook_plot_dataset(self, dataset: xr.Dataset):
        location = self.dataset_config.attrs.location_id
        datastream: str = self.dataset_config.attrs.datastream

        date, time = get_start_date_and_time_str(dataset)

        plt.style.use("default")  # clear any styles that were set before
        plt.style.use("shared/styling.mplstyle")

        with self.storage.uploadable_dir(datastream) as tmp_dir:

            fig, ax = plt.subplots()

            avg_roll = f"= {dataset['roll'].data.mean():.3f} deg]"
            avg_pitch = f"= {dataset['pitch'].data.mean():.3f} deg]"
            roll_label = r"$\.{\theta}_{roll}$ [$\overline{\theta}_r$" + avg_roll
            pitch_label = r"$\.{\theta}_{pitch}$ [$\overline{\theta}_p$" + avg_pitch

            dataset["roll"].plot.hist(bins=100,
                ax=ax, edgecolor="black", histtype="step", label=roll_label,
            )
            dataset["pitch"].plot.hist(bins=100,
                ax=ax, edgecolor="red", histtype="step", label=pitch_label,
            )

            fig.suptitle(f"Buoy Motion Histogram at {location} on {date} {time}")
            ax.set_xlabel("Buoy Motion (deg)")
            ax.set_ylabel("Count")
            ax.set_title("")
            ax.set_xlim(-25, 25)
            ax.legend(ncol=2, bbox_to_anchor=(1, -0.04))

            plot_file = get_filename(
                dataset, title="buoy_motion_histogram", extension="png"
            )
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)
