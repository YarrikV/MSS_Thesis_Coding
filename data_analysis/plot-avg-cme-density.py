import os
import glob
import os
import matplotlib.pyplot as plt


folder = os.path.join("..", "data")
folder = ""

runs = []

# get list of all runs mass111, ..., mass333
for i in range(1, 4):
    for j in range(1, 4):
        for k in range(1, 4):
            run = "mass" + str(i) + str(j) + str(k)
            runs.append(run)

# Loop through all files in the directory that contain "mass" in their filename
for file_path in glob.glob("*.txt"):
    # Do something with the file, such as print its filename
    print(file_path)

with open("mass111-mass.txt") as f:
    print(f)
