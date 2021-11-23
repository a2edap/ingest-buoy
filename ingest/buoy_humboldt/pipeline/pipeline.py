import os
import cmocean
import numpy as np
import xarray as xr
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from typing import Dict
from utils import IngestPipeline, add_colorbar, format_time_xticks
from tsdat import DSUtil


class Pipeline(IngestPipeline):
    """--------------------------------------------------------------------------------
    BUOY INGEST INGESTION PIPELINE

    Ingest of 10-minute data from an AXYS Technologies buoy stationed off the coast of Humboldt, CA.

    --------------------------------------------------------------------------------"""

    def hook_customize_raw_datasets(
        self, raw_dataset_mapping: Dict[str, xr.Dataset]
    ) -> Dict[str, xr.Dataset]:
        dod = self.config.dataset_definition
        time_def = dod.get_variable("time")

        for filename, dataset in raw_dataset_mapping.items():
            if "surfacetemp" in filename:
                old_name = "Surface Temperature (C)"
                new_name = "surfacetemp - Surface Temperature (C)"
                raw_dataset_mapping[filename] = dataset.rename_vars(
                    {old_name: new_name}
                )

            if "gill" in filename:
                name_mapping = {
                    "Horizontal Speed (m/s)": "gill_horizontal_wind_speed",
                    "Horizontal Direction (deg)": "gill_horizontal_wind_direction",
                }
                raw_dataset_mapping[filename] = dataset.rename_vars(name_mapping)

            if "currents" in filename:

                def has_vel_and_dir(index: int) -> bool:
                    has_vel = f"Vel{index+1} (mm/s)" in dataset.variables
                    has_dir = f"Dir{index+1} (deg)" in dataset.variables
                    return has_vel and has_dir

                # Calculate depths and collect data vars
                i = 0
                depth, vel_data, dir_data = [], [], []
                while has_vel_and_dir(i):
                    depth.append(4 * (i + 1))
                    vel_data.append(dataset[f"Vel{i+1} (mm/s)"].data)
                    dir_data.append(dataset[f"Dir{i+1} (deg)"].data)
                    i += 1

                depth = np.array(depth)
                vel_data = np.array(vel_data).transpose()
                dir_data = np.array(dir_data).transpose()

                # Make time.input.name and depth coordinate variables
                dataset = dataset.set_coords(time_def.get_input_name())
                dataset["depth"] = xr.DataArray(data=depth, dims=["depth"])
                dataset = dataset.set_coords("depth")

                # Add current velocity and direction data to dataset
                dataset["current_speed"] = xr.DataArray(
                    data=vel_data, dims=["time", "depth"]
                )
                dataset["current_direction"] = xr.DataArray(
                    data=dir_data, dims=["time", "depth"]
                )

                raw_dataset_mapping[filename] = dataset
        return raw_dataset_mapping

    def hook_generate_and_persist_plots(self, dataset: xr.Dataset):
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
        date = pd.to_datetime(ds.time.data[0]).strftime("%d-%b-%Y")
        loc = ds.attrs["location_meaning"]
        cmap = sns.color_palette("viridis", as_cmap=True)
        colors = [cmap(0.00), cmap(0.60)]

        style_file = os.path.join(os.path.dirname(__file__), "styling.mplstyle")
        with plt.style.context(style_file):

            # Create the first plot -- Surface Met Parameters
            filename = DSUtil.get_plot_filename(
                dataset, "surface_met_parameters", "png"
            )
            with self.storage._tmp.get_temp_filepath(filename) as tmp_path:

                fig, axs = plt.subplots(nrows=3)
                twins = [ax.twinx() for ax in axs]

                # Note gill is done separately (first) so that we can overlay the two
                # sources of wind speed and direction on the same plot (axs[0]).
                double_plot(
                    axs[0],
                    twins[0],
                    data=[ds.gill_wind_speed, ds.gill_wind_direction],
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
                    data=[ds.pressure, ds.rh],
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
                    data=[ds.air_temperature, ds.CTD_SST],
                    colors=colors,
                    var_labels=["Air Temperature", "Sea Surface Temperature"],
                    ax_labels=[
                        r"$\overline{\mathrm{T}}_{air}$ ($\degree$C)",
                        r"$\overline{\mathrm{SST}}$ ($\degree$C)",
                    ],
                )

                fig.suptitle(f"Surface Met Parameters at {loc} on {date}")
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

                fig.savefig(tmp_path)
                self.storage.save(tmp_path)
                plt.close(fig)

            # Create the second plot – conductivity and sea surface temperature
            filename = DSUtil.get_plot_filename(dataset, "conductivity", "png")
            with self.storage._tmp.get_temp_filepath(filename) as tmp_path:

                fig, ax = plt.subplots()
                twin = ax.twinx()

                double_plot(
                    ax,
                    twin,
                    data=[ds.conductivity, ds.CTD_SST],
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
                    f"Conductivity and Sea Surface Temperature at {loc} on {date}"
                )
                format_time_xticks(ax)
                ax.set_xlabel("Time (UTC)")
                ax.grid(which="both", color="lightgray", linewidth=0.5)
                lines = ax.lines + twin.lines
                labels = [line.get_label() for line in lines]
                ax.legend(lines, labels, ncol=len(labels), bbox_to_anchor=(1, -0.03))

                fig.savefig(tmp_path)
                self.storage.save(tmp_path)
                plt.close(fig)

            # Create the third plot - current velocities
            filename = DSUtil.get_plot_filename(dataset, "current_velocity", "png")
            with self.storage._tmp.get_temp_filepath(filename) as tmp_path:

                ds_1H: xr.Dataset = ds.reindex({"depth": ds.depth.data[::2]})
                ds_1H: xr.Dataset = ds_1H.resample(time="1H").nearest()

                # Calculate U&V components of wind vector for a subset of data
                idx = slice(1, None)
                qv_degrees = ds_1H.current_direction.data[idx, idx].transpose()
                qv_theta = (qv_degrees + 90) * (np.pi / 180)
                X, Y = ds_1H.time.data[idx], ds_1H.depth.data[idx]
                U, V = np.cos(-qv_theta), np.sin(-qv_theta)

                fig, ax = plt.subplots()
                csf = ds.current_speed.plot.contourf(
                    ax=ax,
                    x="time",
                    yincrease=False,
                    levels=30,
                    cmap=cmocean.cm.deep_r,
                    add_colorbar=False,
                )
                ax.quiver(
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

                fig.suptitle(f"Current Speed and Direction at {loc} on {date}")
                add_colorbar(ax, csf, r"Current Speed (mm s$^{-1}$)")
                format_time_xticks(ax)
                ax.set_xlabel("Time (UTC)")
                ax.set_ylabel("Depth (m)")

                fig.savefig(tmp_path)
                self.storage.save(tmp_path)
                plt.close(fig)
