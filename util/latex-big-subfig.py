from Euhforia_Run import ALL_FOLDERS

SUBFIG_TEXTWIDTH_FACTOR = 0.3


def print_for_subfig(run_id, bool_eol):
    print("\\begin{subfigure}{" +
          str(SUBFIG_TEXTWIDTH_FACTOR) + "\\textwidth}")
    print("\t\\centering")
    print(
        "\t\\includegraphics[width=\\linewidth]{gfx/Images/research/flux/erosion/Poloidal" + str(run_id) + "_Erosion_plot_fits.png}")
    # print("\t\\caption{"+str(run_id) + "}")
    # print("\t\\label{app_fig:flux"+str(run_id)+"}")
    if bool_eol:
        print("\\end{subfigure}\\\\")
    else:
        print("\\end{subfigure}%")
        # print("\\hfill")


for i, run_name in enumerate(ALL_FOLDERS):
    run_id = run_name[-3:]

    print_for_subfig(run_id, i % 3 == 2)
