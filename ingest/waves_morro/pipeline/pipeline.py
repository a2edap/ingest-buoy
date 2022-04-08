import os
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

from cmocean.cm import amp_r, dense, haline
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
        loc = ds.attrs["location_meaning"]
        date = pd.to_datetime(ds.time.data[0]).strftime("%d-%b-%Y")

        style_file = os.path.join(os.path.dirname(__file__), "styling.mplstyle")
        with plt.style.context(style_file):

            filename = DSUtil.get_plot_filename(dataset, "wave_statistics", "png")
            with self.storage._tmp.get_temp_filepath(filename) as tmp_path:

                fig, axs = plt.subplots(nrows=3)
                fig.suptitle(f"Wave Statistics at {loc} on {date}")

                # Plot Wave Heights
                c1, c2, c3 = amp_r(0.10), amp_r(0.50), amp_r(0.85)
                ds.mean_wave_height.plot(ax=axs[0], c=c1, label=r"H$_{mean}$")
                ds.significant_wave_height.plot(ax=axs[0], c=c2, label=r"H$_{sig}$")
                ds.max_wave_height.plot(ax=axs[0], c=c3, label=r"H$_{max}$")
                axs[0].legend(bbox_to_anchor=(1, -0.10), ncol=3)
                axs[0].set_ylabel("Wave Height (m)")

                # Plot Wave Periods
                c1, c2, c3 = dense(0.15), dense(0.50), dense(0.8)
                ds.mean_wave_period.plot(ax=axs[1], c=c1, label=r"T$_{mean}$")
                ds.peak_wave_period.plot(ax=axs[1], c=c2, label=r"T$_{peak}$")
                ds.max_wave_period.plot(ax=axs[1], c=c3, label=r"T$_{max}$")
                axs[1].legend(bbox_to_anchor=(1, -0.10), ncol=3)
                axs[1].set_ylabel("Wave Period (s)")

                # Plot Wave Directions
                c1, c2 = haline(0.15), haline(0.4)
                ds.mean_wave_direction.plot(ax=axs[2], c=c1, label=r"$\theta_{mean}$")
                ds.peak_wave_direction.plot(ax=axs[2], c=c2, label=r"$\theta_{peak}$")
                axs[2].legend(bbox_to_anchor=(1, -0.10))
                axs[2].set_ylabel("Wave Direction (deg)")

                for i in range(3):
                    axs[i].set_xlabel("Time (UTC)")
                    format_time_xticks(axs[i])

                fig.savefig(tmp_path)
                self.storage.save(tmp_path)
                plt.close(fig)
