from Euhforia_Run import *
from tqdm.auto import tqdm
import os
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


root_path = os.path.join(os.path.expanduser(
    "~"), "local_thesis", "scratch_11_4")
euhforia_events_path = os.path.join(
    root_path, "euhforia_events")

for run_name in tqdm(ALL_FOLDERS):
    run_path = os.path.join(
        euhforia_events_path, run_name, "dat"
    )
    run = Euhforia_Run(run_path, run_name, data_path_from_root(
        root_path), gfx_path_from_root(root_path), max_size=0)
    run.calcFlux()
    run.calcFlux_Toroidal()
