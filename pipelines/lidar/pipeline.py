import xarray as xr
import numpy as np
import cmocean
import matplotlib.pyplot as plt
from typing import Dict

from tsdat import IngestPipeline, get_start_date_and_time_str, get_filename
from utils import add_colorbar, format_time_xticks


class Lidar(IngestPipeline):
    """--------------------------------------------------------------------------------
    LIDAR INGESTION PIPELINE

    Ingest of Lidar data from an AXYS Technologies buoy stationed off the coast of
    Humboldt, CA.

    --------------------------------------------------------------------------------"""

    def hook_customize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # Set initial drive position on wind direction
        drive_position = None

        if "morro" in dataset.attrs["location_id"]:
            drive_position = 180
        if "humboldt" in dataset.attrs["location_id"]:
            drive_position = 90

        if drive_position:
            new_direction = dataset["wind_direction"].data + drive_position
            new_direction[new_direction >= 360] -= 360
            dataset["wind_direction"].data = new_direction
            dataset["wind_direction"].attrs[
                "corrections_applied"
            ] = f"Applied {drive_position} degree calibration factor."

        return dataset

    def hook_finalize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset after qc is applied
        # but before it gets saved to the storage area
        return dataset

    def hook_plot_dataset(self, dataset: xr.Dataset):
        ds = dataset
        location = self.dataset_config.attrs.location_id
        datastream: str = self.dataset_config.attrs.datastream

        date, time = get_start_date_and_time_str(dataset)

        plt.style.use("default")  # clear any styles that were set before
        plt.style.use("shared/styling.mplstyle")

        with self.storage.uploadable_dir(datastream) as tmp_dir:

            fig, ax = plt.subplots()
            heights = dataset["height"].data[::3]
            for i, height in enumerate(heights):
                velocity = ds.wind_speed.sel(height=height)
                velocity.plot(
                    ax=ax,
                    linewidth=2,
                    c=cmocean.cm.deep_r(i / len(heights)),
                    label=f"{height} m",
                )

            format_time_xticks(ax)
            ax.legend(
                facecolor="white",
                ncol=len(heights),
                bbox_to_anchor=(1, -0.05),
            )
            ax.set_title("")  # Remove bogus title created by xarray
            fig.suptitle(f"Wind Speed Time Series at {location} on {date} {time}")
            ax.set_ylabel(r"Wind Speed (ms$^{-1}$)")
            ax.set_xlabel("Time (UTC)")

            plot_file = get_filename(dataset, title="wind_speeds", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)

        # Create the second plot – Lidar wind speed and direction at all elevations
        # and a data availability quality metric.
        with self.storage.uploadable_dir(datastream) as tmp_dir:

            # Reduce dimensionality of dataset – otherwise the details are obscured
            ds_1H: xr.Dataset = ds.resample(time="1H").nearest()

            # Calculations for quiver plot
            qv_slice = slice(1, None)  # Start at 1 to prevent overlap with ax border
            qv_degrees = ds_1H.wind_direction.data[qv_slice].transpose()
            qv_theta = (qv_degrees + 90) * (np.pi / 180)
            X, Y = ds_1H.time.data[qv_slice], ds_1H.height.data
            U, V = np.cos(-qv_theta), np.sin(-qv_theta)

            fig, axs = plt.subplots(nrows=2)
            fig.suptitle(f"Wind Speed and Direction at {location} on {date} {time}")

            # Make top subplot – contour + quiver plot for wind speed and direction
            csf = ds.wind_speed.plot.contourf(
                ax=axs[0],
                x="time",
                levels=30,
                cmap=cmocean.cm.deep_r,
                add_colorbar=False,
            )
            axs[0].quiver(
                X,
                Y,
                U,
                V,
                width=0.002,
                scale=60,
                color="white",
                pivot="middle",
                zorder=10,
            )
            add_colorbar(axs[0], csf, r"Wind Speed (ms$^{-1}$)")

            # Make bottom subplot -- heatmap of data availability
            da = ds.data_availability.plot(
                ax=axs[1],
                x="time",
                cmap=cmocean.cm.amp_r,
                add_colorbar=False,
                vmin=0,
                vmax=100,
            )
            add_colorbar(axs[1], da, "Availability (%)")

            for i in range(2):
                format_time_xticks(axs[i])
                axs[i].set_xlabel("Time (UTC)")
                axs[i].set_ylabel("Height ASL (m)")

            plot_file = get_filename(
                dataset, title="wind_speed_and_direction", extension="png"
            )
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)
