import os
import cmocean
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

from typing import Dict
from tsdat import DSUtil
from utils import IngestPipeline, add_colorbar, format_time_xticks


class Pipeline(IngestPipeline):
    """--------------------------------------------------------------------------------
    LIDAR INGESTION PIPELINE

    Ingest of Lidar data from an AXYS Technologies buoy stationed off the coast of
    Humboldt, CA.

    --------------------------------------------------------------------------------"""

    def hook_customize_dataset(
        self, dataset: xr.Dataset, raw_mapping: Dict[str, xr.Dataset]
    ) -> xr.Dataset:
        # Compress row of variables in input into variables dimensioned by time and height
        for raw_filename, raw_dataset in raw_mapping.items():
            if ".sta" in raw_filename:
                raw_categories = [
                    "Wind Speed (m/s)",
                    "Wind Direction (°)",
                    "Data Availability (%)",
                ]
                output_var_names = ["wind_speed", "wind_direction", "data_availability"]
                heights = dataset.height.data
                for category, output_name in zip(raw_categories, output_var_names):
                    var_names = [f"{height}m {category}" for height in heights]
                    var_data = [raw_dataset[name].data for name in var_names]
                    var_data = np.array(var_data).transpose()
                    dataset[output_name].data = var_data
        return dataset

    def hook_generate_and_persist_plots(self, dataset: xr.Dataset):
        style_file = os.path.join(os.path.dirname(__file__), "styling.mplstyle")

        ds = dataset
        date = pd.to_datetime(ds.time.data[0]).strftime("%d-%b-%Y")
        loc = ds.attrs["location_meaning"]

        with plt.style.context(style_file):

            # Create the first plot - Lidar Wind Speeds at several elevations
            filename = DSUtil.get_plot_filename(dataset, "wind_speeds", "png")
            with self.storage._tmp.get_temp_filepath(filename) as tmp_path:

                fig, ax = plt.subplots()
                heights = [40, 90, 140, 200]
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
                fig.suptitle(f"Wind Speed Time Series at {loc} on {date}")
                ax.set_ylabel(r"Wind Speed (ms$^{-1}$)")
                ax.set_xlabel("Time (UTC)")

                fig.savefig(tmp_path)
                self.storage.save(tmp_path)
                plt.close(fig)

            # Create the second plot – Lidar wind speed and direction at all elevations
            # and a data availability quality metric.
            filename = DSUtil.get_plot_filename(
                dataset, "wind_speed_and_direction", "png"
            )
            with self.storage._tmp.get_temp_filepath(filename) as tmp_path:

                # Reduce dimensionality of dataset – otherwise the details are obscured
                ds_1H: xr.Dataset = ds.resample(time="1H").nearest()

                # Calculations for quiver plot
                qv_slice = slice(
                    1, None
                )  # Start at 1 to prevent overlap with ax border
                qv_degrees = ds_1H.wind_direction.data[qv_slice].transpose()
                qv_theta = (qv_degrees + 90) * (np.pi / 180)
                X, Y = ds_1H.time.data[qv_slice], ds_1H.height.data
                U, V = np.cos(-qv_theta), np.sin(-qv_theta)

                fig, axs = plt.subplots(nrows=2)
                fig.suptitle(f"Wind Speed and Direction at {loc} on {date}")

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

                fig.savefig(tmp_path)
                self.storage.save(tmp_path)
                plt.close(fig)
