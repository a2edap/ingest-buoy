import os
import cmocean
import numpy as np
import xarray as xr
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tsdat import IngestPipeline, get_start_date_and_time_str, get_filename

from utils import format_time_xticks, add_colorbar


class Metocean(IngestPipeline):
    """---------------------------------------------------------------------------------
    This is an example ingestion pipeline meant to demonstrate how one might set up a
    pipeline using this template repository.

    ---------------------------------------------------------------------------------"""

    def hook_customize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset before qc is applied
        return dataset

    def hook_finalize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset after qc is applied
        # but before it gets saved to the storage area
        return dataset

    def hook_plot_dataset(self, dataset: xr.Dataset):
        def double_plot(ax, twin, data, colors, var_labels, ax_labels, **kwargs):
            def _add_lineplot(_ax, _data, _c, _label, _ax_label, _spine):
                _data.plot(ax=_ax, c=_c, label=_label, linewidth=2, **kwargs)
                _ax.tick_params(axis="y", which="both", colors=_c)
                _ax.set_ylabel(_ax_label, color=_c)
                _ax.spines[_spine].set_color(_c)

            _add_lineplot(ax, data[0], colors[0], var_labels[0], ax_labels[0], "left")
            _add_lineplot(
                twin, data[1], colors[1], var_labels[1], ax_labels[1], "right"
            )
            # twin overwrites ax, so set color manually
            twin.spines["left"].set_color(colors[0])

        ds = dataset
        location = self.dataset_config.attrs.location_id
        datastream: str = self.dataset_config.attrs.datastream

        date, time = get_start_date_and_time_str(ds)

        plt.style.use("default")  # clear any styles that were set before
        plt.style.use("shared/styling.mplstyle")
        cmap = sns.color_palette("viridis", as_cmap=True)
        colors = [cmap(0.00), cmap(0.60)]

        # Create the first plot -- Surface Met Parameters
        with self.storage.uploadable_dir(datastream) as tmp_dir:
            fig, axs = plt.subplots(nrows=3)
            twins = [ax.twinx() for ax in axs]

            # Note gill is done separately (first) so that we can overlay the two
            # sources of wind speed and direction on the same plot (axs[0]).
            double_plot(
                axs[0],
                twins[0],
                data=[ds.wind_speed_gill, ds.wind_direction_gill],
                colors=colors,
                var_labels=[
                    r"$\overline{\mathrm{U}}$ Gill",
                    r"$\overline{\mathrm{\theta}}$ Gill",
                ],
                ax_labels=["", ""],
                linestyle="--",
            )
            double_plot(
                axs[0],
                twins[0],
                data=[ds.wind_speed, ds.wind_direction],
                colors=colors,
                var_labels=[
                    r"$\overline{\mathrm{U}}$ Cup",
                    r"$\overline{\mathrm{\theta}}$ Cup",
                ],
                ax_labels=[
                    r"$\overline{\mathrm{U}}$ (ms$^{-1}$)",
                    r"$\bar{\mathrm{\theta}}$ (degrees)",
                ],
            )
            double_plot(
                axs[1],
                twins[1],
                data=[ds.pressure, ds.relative_humidity],
                colors=colors,
                var_labels=["Pressure", "Relative Humidity"],
                ax_labels=[
                    r"$\overline{\mathrm{P}}$ (bar)",
                    r"$\overline{\mathrm{RH}}$ (%)",
                ],
            )
            double_plot(
                axs[2],
                twins[2],
                data=[ds.air_temperature, ds.sea_surface_temperature_YSI],
                colors=colors,
                var_labels=["Air Temperature", "Sea Surface Temperature"],
                ax_labels=[
                    r"$\overline{\mathrm{T}}_{air}$ ($\degree$C)",
                    r"$\overline{\mathrm{SST}}$ ($\degree$C)",
                ],
            )

            fig.suptitle(f"Surface Met Parameters at {location} on {date} {time}")
            twins[0].set_ylim(0, 360)
            for i in range(3):
                axs[i].grid(which="both", color="lightgray", linewidth=0.5)
                lines = axs[i].lines + twins[i].lines
                labels = [line.get_label() for line in lines]
                axs[i].legend(
                    lines, labels, ncol=len(labels), bbox_to_anchor=(1, -0.15)
                )
                format_time_xticks(axs[i])
                axs[i].set_xlabel("Time (UTC)")

            plot_file = get_filename(
                dataset, title="surface_met_parameters", extension="png"
            )
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)

        # Create the second plot – conductivity and sea surface temperature
        with self.storage.uploadable_dir(datastream) as tmp_dir:
            fig, ax = plt.subplots()
            twin = ax.twinx()

            double_plot(
                ax,
                twin,
                data=[ds.conductivity, ds.sea_surface_temperature_CTD],
                colors=colors,
                var_labels=[
                    r"Conductivity (S m$^{-1}$)",
                    r"$\overline{\mathrm{SST}}$ ($\degree$C)",
                ],
                ax_labels=[
                    r"Conductivity (S m$^{-1}$)",
                    r"$\overline{\mathrm{SST}}$ ($\degree$C)",
                ],
            )

            fig.suptitle(
                f"Conductivity and Sea Surface Temperature at {location} on {date}"
            )
            format_time_xticks(ax)
            ax.set_xlabel("Time (UTC)")
            ax.grid(which="both", color="lightgray", linewidth=0.5)
            lines = ax.lines + twin.lines
            labels = [line.get_label() for line in lines]
            ax.legend(lines, labels, ncol=len(labels), bbox_to_anchor=(1, -0.03))

            plot_file = get_filename(dataset, title="conductivity", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)

            # Create the third plot - current velocities
        with self.storage.uploadable_dir(datastream) as tmp_dir:
            fig, ax = plt.subplots(
                nrows=2, ncols=1, figsize=(14, 8), constrained_layout=True
            )
            fig.suptitle(f"Current Speed and Direction at {location} on {date} {time}")

            date = pd.to_datetime(ds["time"].values)
            magn = ax[0].pcolormesh(
                date,
                -ds["depth"],
                ds["current_speed"],
                cmap="Blues",
                shading="nearest",
            )
            ax[0].set_xlabel("Time (UTC)")
            ax[0].set_ylabel(r"Range [m]")
            format_time_xticks(ax[0])
            add_colorbar(ax[0], magn, r"Current Speed (m s$^{-1}$)")

            dirc = ax[1].pcolormesh(
                date,
                -ds["depth"],
                ds["current_direction"],
                cmap="twilight",
                shading="nearest",
            )
            ax[1].set_xlabel("Time (UTC)")
            ax[1].set_ylabel(r"Depth [m]")
            format_time_xticks(ax[1])
            add_colorbar(ax[1], dirc, r"Direction [deg from N]")

            plot_file = get_filename(dataset, title="current_velocity", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)

