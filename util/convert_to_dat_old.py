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

import argparse
import os
import sys
import glob
import re
import numpy as np

import os
import sys

# Add CoCo and EUHFORIA root directories
# NOTE: this assumes default installation directories. Edit if needed

sys.path.append("/data/gent/440/vsc44090/euhforia_feb/coco")
sys.path.append("/data/gent/440/vsc44090/euhforia_feb/euhforia")
sys.path.append("/data/gent/440/vsc44090/euhforia_feb/euhforia/external/pyfishpack")

try:
    evtk = __import__("evtk.hl", fromlist=["gridToVTK"])
except ImportError:
    evtk = __import__("pyevtk.hl", fromlist=["gridToVTK"])

import coco.core.grid
import euhforia.core.io
import euhforia.core.constants as constants


if __name__ == "__main__":


    #
    # Parse command line arguments
    #
    parser = argparse.ArgumentParser()

    # Where the data is located
    parser.add_argument("files",
                        type=str,
                        #metavar="path",
                        nargs="*",
                        help="files to process")

    # Where to save plots and data
    parser.add_argument("--output_dir",
                        default="output/",
                        type=str,
                        metavar="path",
                        help="dir. where output is saved (default: %(default)s)")


    args = parser.parse_args()

    # Display help message if no files given
    if len(args.files) == 0:
        parser.print_help()

    # Get directory of data
    data_dir = os.path.dirname(os.path.abspath(args.files[0]))

    #
    # Create list of file expressions of type xxx_dateTtime*
    #
    file_expressions = []
    for f in args.files:

        # Get the date
        match = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}', f)
        date  = match.group()

        # Split the file name
        fs = f.split(date)

        # Create the file expression
        file_expressions.append(fs[0]+date+"*")
    


    # Remove duplicate and sort
    file_expressions = sorted(list(set(file_expressions)))

    ctr_plt=[]
    #
    # Process each file
    #
    for idx, f in enumerate(file_expressions):

        print ("Processing", f)
        sys.stdout.flush()

        # Load data
        data = euhforia.core.io.load_heliospheric_data(f)

        # Infer date
        date = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}', f).group()
        #print (type(date), type(date[0]), date[0:5])
        # Create cell-centered in-domain data for vtk output
        ng = data.grid.num_ghost_cells

        Br_avg   = 0.5*(data.Br[1::,:,:] + data.Br[0:-1,:,:])
        Bclt_avg = 0.5*(data.Bclt[:,1::,:] + data.Bclt[:,0:-1,:])
        Blon_avg = 0.5*(data.Blon[:,:,1::] + data.Blon[:,:,0:-1])

        in_domain = (slice(ng[0], -ng[0]), slice(ng[1], -ng[1]), slice(ng[2], -ng[2]))

        cell_centered_data \
            = {"vr"   : np.copy(data.vr[in_domain]),
               "vclt" : np.copy(data.vclt[in_domain]),
               "vclt" : np.copy(data.vclt[in_domain]),
               "vlon" : np.copy(data.vlon[in_domain]),
               "n"    : np.copy(data.n[in_domain]),
               "P"    : np.copy(data.P[in_domain]),
               "Br"   : np.copy(Br_avg[in_domain]),
               "Bclt" : np.copy(Bclt_avg[in_domain]),
               "Blon" : np.copy(Blon_avg[in_domain])
               }

        leni = len(data.grid.indomain_center_coords.r/constants.astronomical_unit)
        lenj = len(data.grid.indomain_center_coords.clt)                       
        lenk = len(data.grid.indomain_center_coords.lon)

        k = data.grid.indomain_center_coords.r/constants.astronomical_unit
        i = data.grid.indomain_center_coords.clt
        j = data.grid.indomain_center_coords.lon

        # flattened position arrays
        meshi, meshj, meshk = np.meshgrid(i,j,k)
        coordi   = np.ndarray.flatten(meshi)
        coordj   = np.ndarray.flatten(meshj)
        coordk   = np.ndarray.flatten(meshk)

        # flattened variabile arrays 
        vr = np.ndarray.flatten(data.vr[in_domain], 'F')
        vclt = np.ndarray.flatten(data.vclt[in_domain], 'F')
        vlon = np.ndarray.flatten(data.vlon[in_domain], 'F')
        n = np.ndarray.flatten(data.n[in_domain], 'F')
        P = np.ndarray.flatten(data.P[in_domain], 'F')
        Br = np.ndarray.flatten(Br_avg[in_domain], 'F')
        Bclt = np.ndarray.flatten(Bclt_avg[in_domain], 'F')
        Blon = np.ndarray.flatten(Blon_avg[in_domain], 'F')
        #ctr_plt = np.linspace(0,len(Blon),len(Blon))
        #print (coordk[0])

        

        # Write to DAT file
        f = open(args.output_dir + "/"+ date + ".dat", "w+")
        f.write("TITLE     = \"created from EUHFORIA npz files\" "+"\n")
        f.write("VARIABLES = \"data\"\"r\""+"\n") #("VARIABLES = \"r\""+"\n")
        f.write("\"th\""+"\n")
        f.write("\"ph\""+"\n")
        f.write("\"vr\" \"vclt\" \"vlon\" \"n\" \"P\" \"Br\" \"Bclt\" \"Blon\""+"\n")         
        f.write("ZONE T=\"Rectangular zone\""+"\n")
        f.write("STRANDID=0, SOLUTIONTIME=0"+"\n")                    
        f.write("I="+str(leni)+", J="+str(lenj)+", K="+str(lenk)+", ZONETYPE=Ordered"+"\n")
        f.write("DATAPACKING=POINT"+"\n")
        f.write("DT=(SINGLE SINGLE SINGLE SINGLE )"+"\n")
        np.savetxt( f,  \
                    np.c_[coordk, coordi, coordj, vr, vclt, vlon, n, P, Br, Bclt, Blon]) 

        f.close()
