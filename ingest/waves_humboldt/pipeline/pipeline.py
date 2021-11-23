import os
import cmocean
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

from tsdat import DSUtil
from utils import IngestPipeline, format_time_xticks


class Pipeline(IngestPipeline):
    """--------------------------------------------------------------------------------
    WAVES INGEST INGESTION PIPELINE

    Ingest of 20-minute averaged waves dat from an AXYS Technologies buoy in Humboldt Bay,
    CA.

    --------------------------------------------------------------------------------"""

    def hook_generate_and_persist_plots(self, dataset: xr.Dataset):
        ds = dataset
        date = pd.to_datetime(ds.time.data[0]).strftime("%d-%b-%Y")

        style_file = os.path.join(os.path.dirname(__file__), "styling.mplstyle")
        with plt.style.context(style_file):

            filename = DSUtil.get_plot_filename(dataset, "wave_statistics", "png")
            with self.storage._tmp.get_temp_filepath(filename) as tmp_path:

                # Create figure and axes objects
                fig, axs = plt.subplots(
                    nrows=3, figsize=(14, 8), constrained_layout=True
                )
                fig.suptitle(
                    f"Wave Statistics at {ds.attrs['location_meaning']} on {date}"
                )

                # Plot wave heights
                cmap = cmocean.cm.amp_r
                ds.average_wave_height.plot(
                    ax=axs[0], c=cmap(0.10), linewidth=2, label=r"H$_{avg}$"
                )
                ds.significant_wave_height.plot(
                    ax=axs[0], c=cmap(0.5), linewidth=2, label=r"H$_{sig}$"
                )
                ds.max_wave_height.plot(
                    ax=axs[0], c=cmap(0.85), linewidth=2, label=r"H$_{max}$"
                )
                axs[0].set_ylabel("Wave Height (m)")
                axs[0].legend(bbox_to_anchor=(1, -0.10), ncol=3)

                # Plot wave periods
                cmap = cmocean.cm.dense
                ds.average_wave_period.plot(
                    ax=axs[1], c=cmap(0.15), linewidth=2, label=r"T$_{avg}$"
                )
                ds.significant_wave_period.plot(
                    ax=axs[1], c=cmap(0.5), linewidth=2, label=r"T$_{sig}$"
                )
                ds.mean_wave_period.plot(
                    ax=axs[1], c=cmap(0.8), linewidth=2, label=r"$\overline{T}_{mean}$"
                )
                axs[1].set_ylabel("Wave Period (s)")
                axs[1].legend(bbox_to_anchor=(1, -0.10), ncol=3)

                # Plot mean direction
                cmap = cmocean.cm.haline
                ds.mean_wave_direction.plot(
                    ax=axs[2],
                    c=cmap(0.4),
                    linewidth=2,
                    label=r"$\overline{\phi}_{mean}$",
                )
                axs[2].set_ylabel(r"Wave $\overline{\phi}$ (deg)")
                axs[2].legend(bbox_to_anchor=(1, -0.10))

                # Set xlabels and ticks
                for i in range(3):
                    axs[i].set_xlabel("Time (UTC)")
                    format_time_xticks(axs[i])

                # Save figure
                fig.savefig(tmp_path, dpi=100)
                self.storage.save(tmp_path)
                plt.close()
