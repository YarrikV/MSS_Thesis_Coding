import os
from glob import glob
import tecplot as tp
from tqdm import tqdm

# ! assume all plt files are at least 1 hour separated in time.

all_folders = [
    "mass111",
    "mass112",
    "mass113",
    "mass121",
    "mass122",
    "mass123",
    "mass131",
    "mass132",
    "mass133",
    "mass211",
    "mass212",
    "mass213",
    "mass221",
    "mass222",
    "mass223",
    "mass231",
    "mass232",
    "mass233",
    "mass311",
    "mass312",
    "mass313",
    "mass321",
    "mass322",
    "mass323",
    "mass331",
    "mass332",
    "mass333",
]
folders_to_calc_for = all_folders

PARENT_FOLDER = "euhforia_events"  # folder where the folders_to_calc_for reside
# folder where relative data resides to compare with
RELATIVE_TO_FOLDER = "cmeLess"

for folder in tqdm(folders_to_calc_for):
    path = os.path.join(PARENT_FOLDER, folder, "dat")

    for file in os.listdir(path):
        if file.endswith(".plt"):
            # find plt file to calc relative to:
            # ! file[:-9] is to remove minutes and seconds of file name since these change between the run and the relative run
            relative_path = [
                f
                for f in glob(
                    os.path.join(
                        PARENT_FOLDER, RELATIVE_TO_FOLDER, "dat", file[:-9] + "*.plt"
                    )
                )
            ][0]

            # ! the order of original data and relative data has to be conserved!
            # load plt data
            data = tp.data.load_tecplot(
                os.path.join(path, file),
                read_data_option=tp.constant.ReadDataOption.Replace,
            )

            print(
                "calculating density relative:",
                relative_path,
                " relative to",
                relative_path[-24:-4],
            )

            # load relative plt data
            tp.data.load_tecplot(relative_path)

            # calculate relative density
            tp.data.operate.execute_equation(
                "{n_rel}=({n}[1] - {n}[2])/({n}[2])", [0])

            # save plt data, only first zone (ignoring rel data set)
            tp.data.save_tecplot_plt(os.path.join(path, file), zones=[0])
