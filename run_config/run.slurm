#!/bin/bash
#SBATCH --account="default_project"
#SBATCH --job-name="xxxxx"
#SBATCH --mail-type="END,FAIL,TIME_LIMIT"
#SBATCH --mail-user="yarrik.vanwalleghem@student.kuleuven.be"
#SBATCH --nodes="2"
#SBATCH --ntasks-per-node="72"
#SBATCH --time="12:00:00"

module --force purge
module use /data/leuven/440/vsc44090/easybuild/modules/all/   ### THIS NEED TO BE MODIFIED
module load EUHFORIA
module load coco
#module use  /apps/leuven/icelake/2021a/modules/all/

APP=heliosphere.py # This is inside Easybuild folder
NAME=xxxxx

APP_DIR=$VSC_DATA/euhforia_feb/euhforia/run #Where EUHFORIA is installed
EV_DIR=$VSC_DATA/euhforia_feb/euhforia/run/mass/$NAME
WORK_DIR=$VSC_SCRATCH/euhforia_events/$NAME #Where output will be saved CHANGE TO SCRATCH!


mkdir -p $WORK_DIR
mkdir -p $WORK_DIR/output
mkdir -p $WORK_DIR/input

cp -R $EV_DIR/* $WORK_DIR/input

# jump to APP_DIR, and execute!
cd $APP_DIR
echo "$APP"

mpirun -np 144 ./$APP --config-file $EV_DIR/helios.cfg > $WORK_DIR/log.txt
