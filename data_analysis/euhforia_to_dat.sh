#!/bin/bash

for i in {mass113,mass132,mass221,mass233,mass322,mass121,mass133,mass222,mass311,mass323,mass111,mass122,mass211,mass223,mass312,mass331,mass123,mass212,mass231,mass313,mass332,mass112,mass131,mass213,mass232,mass321,mass333,} 
do
        echo $i

NAME=$i

# defining run name string
# NAME = name of certain run
# path where .npz files are 
WORK_DIR=/scratch/leuven/440/vsc44090/euhforia_events/$NAME

TOOL_DIR=$VSC_SCRATCH

###################---------------- Loading euhforia modules ----------------###################
cd $VSC_DATA
source euhforia.sh

cd /apps/leuven/skylake/2018a/software/Euhforia-GUI/euhforia/tools/


###################---------------------- Merging NPZs ----------------------###################
# folder where npz files are stored
merge_from=$WORK_DIR

# folder where you want to store your merged files
mkdir -p $WORK_DIR/merged
merge_to=$WORK_DIR/merged

# merges diff .npzs of same time steps to one single .npz
./merge_npz.py $merge_from/*.npz --output_dir $merge_to/ # *.npz you want to merge

if [ $? -eq 0 ]; then
    echo NPZs merged successfully.
    rm -r $merge_from/*.npz
else
    echo NPZs could not be merged.
fi

# use merged npz files to create some plots or change to own create_plots.py 
/data/gent/440/vsc44090/euhforia_feb/euhforia/run/create_plots.py $WORK_DIR/merged/*.npz --output_dir $WORK_DIR/


'''
###################-------------------- Making vtk files ---------------------###################
convert_from=$WORK_DIR/merged
convert_to=$WORK_DIR/merged

./convert_to_vtk.py $convert_from/*.npz --output_dir $convert_to/

if [ $? -eq 0 ]; then
    echo VTKs made successfully.
    cd $convert_to
    ls *.vtr>>files.visit
else
    echo VTKs could not be made.
fi
'''


echo "Making dat files"
###################---------------------- Making dat files -------------------###################
mkdir -p $WORK_DIR/dat
cd $TOOL_DIR
pwd |& echo

./convert_to_dat.py $WORK_DIR/merged/*.npz --output_dir $WORK_DIR/dat/ #*.npz


echo "Making plt files"
###################-------------------- Making plt files ---------------------###################
# requires dat files
module purge
module load Tecplot

FILES=$WORK_DIR/dat/*.dat

# prepare for tecplot visualization
for f in $FILES
do
  echo "Processing $f file, creating .plt..."
  preplot $f ${f%.dat}.plt
  rm $f
done

done
