import xarray as xr
import act
import matplotlib.pyplot as plt
from tsdat import IngestPipeline, get_start_date_and_time_str, get_filename
from utils import format_time_xticks
from cmocean.cm import amp_r, dense, haline


class Waves(IngestPipeline):
    """--------------------------------------------------------------------------------
    WAVES INGEST INGESTION PIPELINE

    Ingest of 20-minute averaged waves dat from an AXYS Technologies buoy in Humboldt Bay,
    CA.

    --------------------------------------------------------------------------------"""

    def hook_plot_dataset(self, dataset: xr.Dataset):
        ds = dataset
        loc = self.dataset_config.attrs.location_id
        datastream: str = self.dataset_config.attrs.datastream

        date, time = get_start_date_and_time_str(dataset)

        plt.style.use("default")  # clear any styles that were set before
        plt.style.use("shared/styling.mplstyle")

        with self.storage.uploadable_dir(datastream) as tmp_dir:

            fig, axs = plt.subplots(nrows=3)
            fig.suptitle(f"Wave Statistics at {loc} on {date} {time}")

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
            axs[2].legend(bbox_to_anchor=(1, -0.10), ncol=2)
            axs[2].set_ylabel("Wave Direction (deg)")

            for i in range(3):
                axs[i].set_xlabel("Time (UTC)")
                format_time_xticks(axs[i])

            plot_file = get_filename(ds, title="wave_data_plots", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)

            # Creat Plot Display
            obj = ds
            variable = "significant_wave_height"
            display = act.plotting.TimeSeriesDisplay(
                obj, figsize=(15, 10), subplot_shape=(2,)
            )
            # Plot data in top plot
            display.plot(variable, subplot_index=(0,), label="Wave Height")
            # Plot QC data
            display.qc_flag_block_plot(variable, subplot_index=(1,))
            fig = display.fig

            plot_file = get_filename(ds, title="wave_height", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)
