import os
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

from tsdat import DSUtil
from utils import IngestPipeline


class Pipeline(IngestPipeline):
    """--------------------------------------------------------------------------------
    IMU INGEST INGESTION PIPELINE

    Ingest of IMU data from an AXYS Technologies buoy stationed off the coast of
    Humboldt, CA.

    --------------------------------------------------------------------------------"""

    def hook_generate_and_persist_plots(self, dataset: xr.Dataset):
        style_file = os.path.join(os.path.dirname(__file__), "styling.mplstyle")

        loc = dataset.attrs["location_meaning"]
        date = pd.to_datetime(dataset.time.data[0]).strftime("%d-%b-%Y")
        start = pd.to_datetime(dataset.time.data[0]).strftime("%H:%M")
        end = pd.to_datetime(dataset.time.data[-1]).strftime("%H:%M")
        time_range = f"{date} from {start} to {end}"

        with plt.style.context(style_file):

            filename = DSUtil.get_plot_filename(dataset, "buoy_motion_histogram", "png")
            with self.storage._tmp.get_temp_filepath(filename) as tmp_path:

                fig, ax = plt.subplots()

                avg_roll = f"= {dataset['roll'].data.mean():.3f} deg]"
                avg_pitch = f"= {dataset['pitch'].data.mean():.3f} deg]"
                roll_label = r"$\.{\theta}_{roll}$ [$\overline{\theta}_r$" + avg_roll
                pitch_label = r"$\.{\theta}_{pitch}$ [$\overline{\theta}_p$" + avg_pitch

                dataset["roll"].plot.hist(
                    ax=ax,
                    edgecolor="black",
                    histtype="step",
                    label=roll_label,
                )
                dataset["pitch"].plot.hist(
                    ax=ax,
                    edgecolor="red",
                    histtype="step",
                    label=pitch_label,
                )

                fig.suptitle(f"Buoy Motion Histogram at {loc} on {time_range}")
                ax.set_xlabel("Buoy Motion (deg)")
                ax.set_ylabel("Frequency")
                ax.set_title("")
                ax.set_xlim(-25, 25)
                ax.legend(ncol=2, bbox_to_anchor=(1, -0.04))

                fig.savefig(tmp_path)
                self.storage.save(tmp_path)
                plt.close(fig)
