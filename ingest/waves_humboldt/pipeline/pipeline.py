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

                c1, c2, c3 = amp_r(0.10), amp_r(0.50), amp_r(0.85)
                ds.average_wave_height.plot(ax=axs[0], c=c1, label=r"H$_{avg}$")
                ds.significant_wave_height.plot(ax=axs[0], c=c2, label=r"H$_{sig}$")
                ds.max_wave_height.plot(ax=axs[0], c=c3, label=r"H$_{max}$")
                axs[0].legend(bbox_to_anchor=(1, -0.10), ncol=3)
                axs[0].set_ylabel("Wave Height (m)")

                c1, c2, c3 = dense(0.15), dense(0.50), dense(0.80)
                ds.average_wave_period.plot(ax=axs[1], c=c1, label=r"T$_{avg}$")
                ds.significant_wave_period.plot(ax=axs[1], c=c2, label=r"T$_{sig}$")
                ds.mean_wave_period.plot(
                    ax=axs[1], c=c3, label=r"$\overline{T}_{mean}$"
                )
                axs[1].legend(bbox_to_anchor=(1, -0.10), ncol=3)
                axs[1].set_ylabel("Wave Period (s)")

                ds.mean_wave_direction.plot(
                    ax=axs[2], c=haline(0.4), label=r"$\overline{\phi}_{mean}$"
                )
                axs[2].legend(bbox_to_anchor=(1, -0.10))
                axs[2].set_ylabel(r"Wave $\overline{\phi}$ (deg)")

                for i in range(3):
                    axs[i].set_xlabel("Time (UTC)")
                    format_time_xticks(axs[i])

                fig.savefig(tmp_path)
                self.storage.save(tmp_path)
                plt.close(fig)
