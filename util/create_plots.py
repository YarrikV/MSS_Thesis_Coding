#!/usr/bin/env python
#
# This file is part of EUHFORIA.
#
# Copyright 2016, 2017, 2018 Jens Pomoell
#
# EUHFORIA is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# EUHFORIA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EUHFORIA. If not, see <http://www.gnu.org/licenses/>.
import os
import sys
sys.path = sys.path[:-3]
sys.path.append("/data/leuven/323/vsc32397/Euhforia-GUI/coco")
sys.path.append("/data/leuven/323/vsc32397/Euhforia-GUI/euhforia")
sys.path.append("/data/leuven/323/vsc32397/Euhforia-GUI/euhforia/external/pyfishpack")
print(sys.path)

import argparse
import datetime
import glob
import os
import re
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.dates import DateFormatter, DayLocator, HourLocator
from matplotlib.ticker import MultipleLocator

import euhforia.core.constants as constants

# EUHFORIA imports
import euhforia.core.io
import euhforia.orbit
import euhforia.plot.colormap
import euhforia.plot.slice

matplotlib.use("Agg")


if __name__ == "__main__":

    #
    # Parse command line arguments
    #
    parser = argparse.ArgumentParser()

    # Where the data is located
    parser.add_argument(
        "files",
        type=str,
        # metavar="path",
        nargs="*",
        help="files to process",
    )

    # Where to save plots and data
    parser.add_argument(
        "--output_dir",
        default="output/",
        type=str,
        metavar="path",
        help="dir. where output is saved (default: %(default)s)",
    )

    # Which meridional slice to plot
    parser.add_argument(
        "--meridional_plane",
        default="Earth",
        type=str,
        help="Name of object determining which meridional \
                              plane to plot (default: %(default)s)",
    )

    # Which in-situ data to plot
    parser.add_argument(
        "--insitu", default="default", type=str, help="In-situ data to plot: ACE NRT (default), OMNI, None"
    )

    # Plot log density?
    parser.add_argument("--logn", default="False", type=str, help="Plot density on log scale (False/True)")

    parser.add_argument("--lowres", action="store_true")

    args = parser.parse_args()

    # Display help message if no files given
    if len(args.files) == 0:
        parser.print_help()
        exit()

    # Get directory of data
    data_dir = os.path.dirname(os.path.abspath(args.files[0]))

    #
    # Create list of file expressions of type xxx_dateTtime*
    #
    file_expressions = []
    dates = []
    for f in args.files:

        # Get the date
        match = re.search(r"\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}", f)

        # Skip if a file matching the regex does not exist
        if match is not None:

            # Get date of output
            date = match.group()

            dates.append(date)

            # Split the file name
            fs = f.split(date)

            # Create the file expression
            file_expressions.append(fs[0] + date + "*")

    # Remove duplicate and sort
    file_expressions = sorted(list(set(file_expressions)))
    dates = sorted(list(set(dates)))

    # Parse first and last date
    first_date = datetime.datetime.strptime(dates[0], "%Y-%m-%dT%H-%M-%S")
    last_date = datetime.datetime.strptime(dates[-1], "%Y-%m-%dT%H-%M-%S")
    delta_t = (last_date - first_date).days

    #
    # Instantiate planets and spacecraft
    #
    mercury = euhforia.orbit.Mercury()
    venus = euhforia.orbit.Venus()
    earth = euhforia.orbit.Earth()
    mars = euhforia.orbit.Mars()
    sta = euhforia.orbit.STA()
    stb = euhforia.orbit.STB()
    psp = euhforia.orbit.PSP()
    solo = euhforia.orbit.SOLO()
    heliospheric_objects = (mercury, venus, earth, mars, sta, stb, psp, solo)

    # virtual spacecraft
    vs = getattr(euhforia.orbit, args.meridional_plane)()

    #
    # Virtual spacecraft time series data
    #

    # Determine which time series file to open
    simulation_time_series_file = None
    for f in glob.glob(data_dir + "/*.dsv"):
        if args.meridional_plane in f:
            simulation_time_series_file = f

    # Load the data if .dsv files have been found
    df = None
    if simulation_time_series_file is not None:
        print("Loading", simulation_time_series_file)

        df = pd.read_csv(simulation_time_series_file, sep=r"\s+", parse_dates=["date"])

        # If dsv file exists but no data is stored, make it None
        df = df if len(df) > 1 else None

    #
    # Spacecraft in-situ data
    #

    # Which in-situ data to plot
    insitu_dataset = args.insitu.lower()

    # Plot in-situ data?
    plot_time_series = False #if insitu_dataset == "none" else True
    plot_insitu = plot_time_series
    if first_date == last_date:
        plot_time_series = False

    #plot_insitu = False
    #plot_time_series = False
    # Load in-situ data
    if plot_time_series:

        if insitu_dataset == "default":
            import euhforia.insitu.rt

            insitu = euhforia.insitu.rt.ACERealTimeData(data_dir + "/ace_data/")
        elif insitu_dataset == "omni":
            import euhforia.insitu.omni

            insitu = euhforia.insitu.omni.OMNIData()
        else:
            raise ValueError("Unknown in-situ dataset " + insitu_dataset)

        insitu.start_time = first_date  # df['date'].iloc[0]
        insitu.end_time = last_date  # df['date'].iloc[-1]

        print("Loading", insitu.label, "data")
        try:
            insitu.retrieve()
        except OSError:
            plot_insitu = False

    for idx, f in enumerate(file_expressions):

        print("Processing", f)
        sys.stdout.flush()

        # Load data
        data = euhforia.core.io.load_heliospheric_data(f)

        date = re.search(r"\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}", f).group()

        # Meridional plane to slice
        lon_slice = vs.position(data.datetime.item(0))[2]

        fig = plt.figure(figsize=(10, 7))

        gs = matplotlib.gridspec.GridSpec(2, 2, width_ratios=[1.38, 1.0], height_ratios=[3, 1])

        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        ax3 = plt.axes((0.135, 0.08, 0.67, 0.14))

        #
        # Create plot of the radial speed
        #
        euhforia.plot.slice.equatorial_and_meridional(
            data,
            variable="vr",
            meridional_slice=lon_slice,
            levels=np.linspace(200, 1600, 120),
            cmap=euhforia.plot.colormap.citrus,
            heliospheric_objects=heliospheric_objects,
            colorbar_ticks=np.linspace(200, 1600, 8),
            fig=fig,
            ax=(ax1, ax2),
        )

        ax2.set_xlim([0, data.grid.indomain_edge_coords.r[-1]/constants.astronomical_unit])

        #
        # Add time series line plot
        #
        if plot_time_series:

            if df is not None:
                ax3.plot(df["date"], df["vr[km/s]"], "b", label="EUHFORIA")

            if plot_insitu:
                ax3.plot(insitu.df["date"], insitu.df["flow_speed"]/1e3, "-r", label=insitu.label, lw=2, alpha=0.7)
            ax3.plot([data.datetime.item(0), data.datetime.item(0)], [0, 4000], "-k", lw=2, alpha=0.5)

            ax3.set_ylim((200, 1000))
            ax3.set_xlim((first_date, last_date))

            ax3.set_ylabel("Speed [km/s]")

            ax3.yaxis.set_tick_params(labelsize=9)
            ax3.xaxis.set_tick_params(labelsize=12)

            ax3.yaxis.set_major_locator(MultipleLocator(200))
            ax3.yaxis.set_minor_locator(MultipleLocator(100))

            if delta_t < 4:
                ax3.xaxis.set_minor_locator(HourLocator(np.arange(0, 25)))
                ax3.xaxis.set_major_formatter(DateFormatter("%H:%M"))
                ax3.xaxis.set_tick_params(labelsize=10)
            else:
                ax3.xaxis.set_minor_locator(HourLocator(np.arange(0, 25, 6)))
                ax3.xaxis.set_major_formatter(DateFormatter("%b %d"))

            ax3.legend(loc="upper right", bbox_to_anchor=(1.2, 1.05), fontsize=8)

        # Save
        if args.lowres:
            plt.savefig(args.output_dir + "vr_" + date, dpi=72)
        else:
            plt.savefig(args.output_dir + "vr_" + date, dpi=200)
            plt.savefig(args.output_dir + "vr_" + date + ".pdf", dpi=300)

        plt.close("all")

        #
        # Create plot of the scaled number density
        #
        fig = plt.figure(figsize=(10, 7))

        gs = matplotlib.gridspec.GridSpec(2, 2, width_ratios=[1.38, 1.0], height_ratios=[3, 1])
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        ax3 = plt.axes((0.135, 0.08, 0.67, 0.14))

        nscaled = np.zeros(data.n.shape)
        for idx, r in enumerate(data.grid.center_coords.r):
            nscaled[idx, :, :] = data.n[idx, :, :] * (r / constants.astronomical_unit) ** 2

        data.add_variable(nscaled, name=r"$n \, (r / 1 \mathrm{AU})^2$", unit="cm$^{-3}$")

        euhforia.plot.slice.equatorial_and_meridional(
            data,
            variable=r"$n \, (r / 1 \mathrm{AU})^2$",
            meridional_slice=lon_slice,
            levels=np.linspace(0, 60, 120),
            cmap=euhforia.plot.colormap.citrus,
            heliospheric_objects=heliospheric_objects,
            colorbar_ticks=np.linspace(0, 60, 7),
            fig=fig,
            ax=(ax1, ax2),
        )

        ax2.set_xlim([0, data.grid.indomain_edge_coords.r[-1]/constants.astronomical_unit])

        #
        # Add time series line plot
        #
        if plot_time_series:

            # Add line plot
            if args.logn.lower() == "true":
                if df is not None:
                    ax3.semilogy(df["date"], df["n[1/cm^3]"], "b", label="EUHFORIA")

                if plot_insitu:
                    ax3.semilogy(
                        insitu.df["date"],
                        insitu.df["proton_number_density"]/1e6,
                        "-r",
                        label=insitu.label,
                        lw=2,
                        alpha=0.7,
                    )
                ax3.semilogy([data.datetime.item(0), data.datetime.item(0)], [1e-2, 4000], "-k", lw=2, alpha=0.5)
                ax3.set_ylim((0.5, 100))

            else:
                if df is not None:
                    ax3.plot(df["date"], df["n[1/cm^3]"], "b", label="EUHFORIA")

                if plot_insitu:
                    ax3.plot(
                        insitu.df["date"],
                        insitu.df["proton_number_density"]/1e6,
                        "-r",
                        label=insitu.label,
                        lw=2,
                        alpha=0.7,
                    )
                ax3.plot([data.datetime.item(0), data.datetime.item(0)], [0, 4000], "-k", lw=2, alpha=0.5)
                ax3.set_ylim((0, 30))

                ax3.yaxis.set_major_locator(MultipleLocator(10))
                ax3.yaxis.set_minor_locator(MultipleLocator(5))

            ax3.set_xlim((first_date, last_date))

            ax3.set_ylabel("$n$ [cm$^{-3}$]")

            ax3.yaxis.set_tick_params(labelsize=9)
            ax3.xaxis.set_tick_params(labelsize=12)

            if delta_t < 4:
                ax3.xaxis.set_minor_locator(HourLocator(np.arange(0, 25)))
                ax3.xaxis.set_major_formatter(DateFormatter("%H:%M"))
                ax3.xaxis.set_tick_params(labelsize=10)
            else:
                ax3.xaxis.set_minor_locator(HourLocator(np.arange(0, 25, 6)))
                ax3.xaxis.set_major_formatter(DateFormatter("%b %d"))

            ax3.legend(loc="upper right", bbox_to_anchor=(1.2, 1.05), fontsize=8)

        if args.lowres:
            plt.savefig(args.output_dir + "nscaled_" + date, dpi=72)
        else:
            plt.savefig(args.output_dir + "nscaled_" + date, dpi=200)
            plt.savefig(args.output_dir + "nscaled_" + date + ".pdf", dpi=300)

        plt.close("all")

        #
        # Create plot of the Bclt
        #

        fig = plt.figure(figsize=(10, 7))

        gs = matplotlib.gridspec.GridSpec(2, 2, width_ratios=[1.38, 1.0], height_ratios=[3, 1])

        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        ax3 = plt.axes((0.135, 0.08, 0.67, 0.14))

        #
        # Create plot of the Bclt
        #
        euhforia.plot.slice.equatorial_and_meridional(
            data,
            variable="Bclt",
            meridional_slice=lon_slice,
            levels=np.linspace(-15, 15, 120),
            cmap='RdBu', #euhforia.plot.colormap.citrus,
            heliospheric_objects=heliospheric_objects,
            colorbar_ticks=np.linspace(-15, 15, 8),
            fig=fig,
            ax=(ax1, ax2),
        )

        ax2.set_xlim([0, data.grid.indomain_edge_coords.r[-1]/constants.astronomical_unit])

        # Save
        if args.lowres:
            plt.savefig(args.output_dir + "bclt_" + date, dpi=72)
        else:
            plt.savefig(args.output_dir + "bclt_" + date, dpi=200)
            plt.savefig(args.output_dir + "bclt_" + date + ".pdf", dpi=300)

        plt.close("all")

        #
        # Create plot of the Br
        #

        fig = plt.figure(figsize=(10, 7))

        gs = matplotlib.gridspec.GridSpec(2, 2, width_ratios=[1.38, 1.0], height_ratios=[3, 1])

        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        ax3 = plt.axes((0.135, 0.08, 0.67, 0.14))

        #
        # Create plot of the Br
        #
        euhforia.plot.slice.equatorial_and_meridional(
            data,
            variable="Br",
            meridional_slice=lon_slice,
            levels=np.linspace(-15, 15, 120),
            cmap='RdBu', #euhforia.plot.colormap.citrus,
            heliospheric_objects=heliospheric_objects,
            colorbar_ticks=np.linspace(-15, 15, 8),
            fig=fig,
            ax=(ax1, ax2),
        )

        ax2.set_xlim([0, data.grid.indomain_edge_coords.r[-1]/constants.astronomical_unit])

        # Save
        if args.lowres:
            plt.savefig(args.output_dir + "br_" + date, dpi=72)
        else:
            plt.savefig(args.output_dir + "br_" + date, dpi=200)
            plt.savefig(args.output_dir + "br_" + date + ".pdf", dpi=300)

        plt.close("all")

        #
        # Create plot of the Blon
        #

        fig = plt.figure(figsize=(10, 7))

        gs = matplotlib.gridspec.GridSpec(2, 2, width_ratios=[1.38, 1.0], height_ratios=[3, 1])

        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        ax3 = plt.axes((0.135, 0.08, 0.67, 0.14))

        #
        # Create plot of the Blon
        #
        euhforia.plot.slice.equatorial_and_meridional(
            data,
            variable="Blon",
            meridional_slice=lon_slice,
            levels=np.linspace(-15, 15, 120),
            cmap='RdBu', #euhforia.plot.colormap.citrus,
            heliospheric_objects=heliospheric_objects,
            colorbar_ticks=np.linspace(-15, 15, 8),
            fig=fig,
            ax=(ax1, ax2),
        )

        ax2.set_xlim([0, data.grid.indomain_edge_coords.r[-1]/constants.astronomical_unit])

        # Save
        if args.lowres:
            plt.savefig(args.output_dir + "blon_" + date, dpi=72)
        else:
            plt.savefig(args.output_dir + "blon_" + date, dpi=200)
            plt.savefig(args.output_dir + "blon_" + date + ".pdf", dpi=300)

        plt.close("all")
