#!/usr/bin/env python
#
# This file is part of EUHFORIA.
#
# Copyright 2016, 2017 Jens Pomoell
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

import argparse

import euhforia
import euhforia.heliosphere.mhd.heliosphere as ih

if __name__ == "__main__":

    #
    # Parse command line arguments
    #
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config-file", default="heliosphere_default.cfg", type=str, help="Configuration file (default: %(default)s)"
    )

    args = parser.parse_args()

    # Instantiate simulation, use the provided config file for setup
    sim = ih.InnerHeliosphereSimulation(config=args.config_file)

    # Define the computational grid
    sim.set_grid()

    # Initialize the simulation infrastructure
    sim.initialize()

    # Set parameters related to the physics model
    sim.set_solver_parameters()

    # Setup the solar wind boundary data
    sim.initialize_solar_wind_boundary_data()

    # Initialize the solver that computes the inner radial boundary
    # electric field
    sim.initialize_electric_field_solver()

    # Setup run times
    sim.set_simulation_duration()

    # Setup CMEs
    sim.initialize_CMEs()

    # If no CMEs are present, skip CME insertion and reset times
    if len(sim.CMEs.list_of_cmes) == 0:
        sim.set_simulation_duration(skip_cme_insertion=True)

    # Construct initial state
    sim.set_boundary_conditions()
    sim.set_initial_condition()

    # Add output events
    sim.add_output_events()

    # Run the simulation
    sim.print_info_to_screen_at_startup()
    sim.run(**sim.run_kwargs)
