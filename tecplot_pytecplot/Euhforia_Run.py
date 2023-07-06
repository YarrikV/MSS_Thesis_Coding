import logging
import os
import sys
import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *
# ! always snake_case
# ! in macros: indices start from 1
# ! in pytecplot: indices start from 0

ALL_FOLDERS = [
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
TECPLOT_FILES_PATH = os.path.join("python scripts", "tecplot-files")

B_LON_THRESHOLD = 5
B_CLT_THRESHOLD = 2
B_CLT_R_THRESHOLD = 0.11
B_CLT_SCALED_SQ_THRESHOLD = 1


def setup_border_size_position_frame(position, width=3.5, height=2.0, showBorder=False, transparent=True):
    tp.active_frame().plot().frame.position = position
    tp.active_frame().plot().frame.width = width
    tp.active_frame().plot().frame.height = height
    tp.active_frame().plot().frame.show_border = showBorder
    tp.active_frame().plot().frame.transparent = transparent


def setup_view_angle_XY():
    tp.active_frame().plot().view.position = (0, -20.3297, 0)
    tp.active_frame().plot().view.theta = 0
    tp.active_frame().plot().view.position = (0, 0, 20.3297)
    tp.active_frame().plot().view.psi = 0


def data_path_from_root(root_path):
    return os.path.join(root_path, "data")


def gfx_path_from_root(root_path):
    return os.path.join(root_path, "gfx")


def double_slashes(s):
    return "".join([char*2 if char == "\\" else char for char in s])


class Euhforia_Run:
    """Euhforia_Run

    Used to automate analysis of an EUHFORIA run using Tecplot.

    Attributes
    ----------
    log : Logger 
        to log what is happening
    run_name : str
        run ID
    run_path : str
        path of folder where .plt files are stored of the run
    store_data_path : str
        path of folder where data will be stored
    store_gfx_path : str
        path of folder where gfx will be stored
    layout : tecplot.Layout
        tecplot layout where data is being analysed
    size : int
        amount of .plt files = amount of time steps
    timestrands : [str]
        length = amount of strands in the tecplot layout
        str = description of strand (what it is used for etc.)
    """

    def __init__(self, run_path, run_name, store_data_path, store_gfx_path, max_size=0):
        """Initialize Euhforia_Run.

        Args:
            run_path (string): path of folder where .plt are stored.
            store_data_path (string): path of folder where data will be stored.
            store_gfx_path (string): path of folder where gfx will be stored.
        """

        self.run_name = run_name
        self.run_path = run_path
        self.store_data_path = store_data_path
        self.store_gfx_path = store_gfx_path

        self.create_logger()

        # length of a run = amount of plt files = amount of time steps
        self.size = 0

        # timestrands is a list of strings, the strings explain timestrand
        self.timestrands = []
        self.initialise_tp_with_data(max_size)

    def __len__(self):
        return self.size

    def create_logger(self):
        """Initialize Logger
        """

        self.log = logging.getLogger(f"euhforia-run-{self.run_name}")
        self.log.setLevel(logging.DEBUG)

    def initialise_tp_with_data(self, max_size):
        """Initialises Tecplot layout (self.layout) with .plt files.

        Args:
            max_size (int): limits amount of .plt files to this number
        """

        self.layout = tp.new_layout()

        # for file in folder where .plt files are stored
        for file in os.listdir(self.run_path):
            # only process .plt files
            if not file.endswith(".plt"):
                continue

            # process plt file
            # 1/ add to length of the run
            self.size += 1

            # 2/ add data in plt to layout
            self.layout = tp.data.load_tecplot(
                os.path.join(self.run_path, file),
                add_zones_to_existing_strands=True,
                read_data_option=ReadDataOption.Append,
                reset_style=False
            )

            # 3/ check if max files limit is reached
            if max_size > 0 and len(self) == max_size:
                break

        self.log.info(f"Done loading. Loaded {len(self)} .plt files.")

        # initialize frame to be 3d with cartesian coordinates
        self.calculate_vars_position()

        # set time strands of initial data zones (whole simulation)
        self.timestrands.append("initial_data")
        tp.macro.execute_extended_command(
            command_processor_id="Strand Editor",
            command=f"""
            ZoneSet=1-{len(self)};AssignStrands=TRUE;StrandValue={len(self.timestrands)};
            AssignSolutionTime=TRUE;TimeValue=0;DeltaValue=1;TimeOption=ConstantDelta;""",
        )
        self.log.info("Done extracting initial time strands.")

    def calculate_vars_position(self):
        """Calculates xyz variables and sets up 3D plot in first frame.
        """
        tp.macro.execute_file(
            os.path.join(
                TECPLOT_FILES_PATH, "calcEquations_cartesian_SetAxis.mcr")
        )
        self.log.debug(
            f"Done calculating xyz, set 3D axis coordinates to xyz.")

    def performIntegration(self, int_variable, title, strand=0, blanking_enable=[], blanking_disable=[]):
        """Performs scalar integration excluding blanked regions.
        Current frame should be data frame.
        Does opposite blanking after integration: enables regions in blanking_enable,
        but disables those regions after integration.
        Active frame after this function is the frame before the integration.
        Integration excludes blank region with the option "only blank when all corners are blanked"

        Args:
            variable (str): variable over which to integrate
            strand (int, optional): time strand to integrate over. 
                Defaults to 0, which then takes the last strand.
            blankingEnable (list, optional): list of blanking regions to 
                enable before integration. Defaults to [].
            blankingDisable (list, optional): list of blanking regions to  
                disabble before integration. Defaults to [].
        """
        frame = tp.active_frame()

        # if no strand is given, use strand of latest zone
        if strand == 0:
            strand = self.layout.zone(-1).strand

        for blanking in blanking_enable:
            frame.plot().value_blanking.constraint(blanking).active = True

        for blanking in blanking_disable:
            frame.plot().value_blanking.constraint(blanking).active = False

        # ! integration index + 1 because in macros, indices start from 1
        integration_index = self.layout.variable(int_variable).index+1
        tp.macro.execute_extended_command(
            command_processor_id="CFDAnalyzer4",
            command=f"""Integrate [{strand}] VariableOption='Scalar' 
                XOrigin=0 YOrigin=0 ZOrigin=0 
                ScalarVar={integration_index} 
                Absolute='F' ExcludeBlanked='T' 
                XVariable=1 YVariable=2 ZVariable=3 
                IntegrateOver='Cells' IntegrateBy='TimeStrands' 
                IRange={{MIN=1 MAX=0 SKIP=1}} JRange={{MIN=1 MAX=0 SKIP=1}} KRange={{MIN=1 MAX=0 SKIP=1}} 
                PlotResults='T' PlotAs='{title}' 
                TimeMin=0 TimeMax={len(self)-1}""",
        )

        # undo blanking
        for blanking in blanking_enable:
            frame.plot().value_blanking.constraint(blanking).active = False

        for blanking in blanking_disable:
            frame.plot().value_blanking.constraint(blanking).active = True

    def blanking(self, constraint, variable, operator, comparison_value, active=True):
        """Blanks constraint with variable & operator & comparison value.
        Sets active to active.
        This is all being implemented in currently active frame.

        Args:
            constraint (int): denotes which blanking constraint
            variable (str): name of variable
            operator (RelOp. ...): constant denoting operator
            comparison_value (float): self-expl.
            active (bool, optional): sets active to this value. Defaults to True.
        """
        blk = tp.active_frame().plot().value_blanking.constraint(constraint)
        blk.active = active
        blk.variable = self.layout.variable(variable)
        blk.comparison_operator = operator
        blk.comparison_value = comparison_value

    def twoD_plot_fix_axesOnly(self):
        """Sets limits of axes & sets y label to be parallel with axis."""
        tp.active_frame().plot().axes.y_axis(0).fit_range()
        tp.active_frame().plot().axes.x_axis(0).fit_range()
        tp.active_frame().plot().axes.x_axis(0).max += .01 * \
            tp.active_frame().plot().axes.x_axis(0).max

        tp.active_frame().plot().axes.y_axis(
            0).tick_labels.alignment = LabelAlignment.AlongAxis

    def twoD_plot_fix_axes(self, path_to_Stylesheet):
        """Cleans up axes of current frame (must be a 2D plot).
        Loads stylesheet, set limits of axes and sets label to be parallel.
        RedrawsAll at end.

        Args:
            pathStylesheet (str): path to stylesheet to load.
        """

        tp.active_frame().load_stylesheet(path_to_Stylesheet)
        self.twoD_plot_fix_axesOnly()

        tp.macro.execute_command('$!RedrawAll')

    def calcFlux(self, Bclt_threshold=B_CLT_THRESHOLD, r_threshold=B_CLT_R_THRESHOLD, doMinus=True, doPlus=True):
        """Calculates flux of both sides of the CME depending on the threshold 
        value given.

        1) Set up slice
        2) Extract equatorial plane slice for every time step 
        3) Set up time strands
        4) Set up blanking
        5) Does integration
        6) Saves images
        7) Saves data

        Args:
            Bclt_threshold (int, optional): absolute value of threshold
                used for flux integration of both sides of CME. Defaults to 2.
            r_threshold (int, optional): value of threshold for r. Blanking is 
                done for values lower or equal than this value. Defaults to 0.11.
            doMinus (bool): control if minus side of flux integration is done.
            doPlus (bool): control if plus side of flux integration is done.  
        """
        logger = self.log.getChild("fluxCalc_Poloidal")
        logger.setLevel = logging.DEBUG
        tp.macro.execute_command(
            '''$!FrameControl ActivateByNumber Frame = 1''')
        plot = tp.active_frame().plot()

        # 1) Set up slice
        plot.slice(0).orientation = SliceSurface.ZPlanes
        plot.slice(0).origin.z = 0

        # 2) Extract equatorial plane slice for every time step
        # 3) Set up time strands
        self.timestrands.append("slices_at_equatorial")
        plot.slices(0).extract(
            transient_mode=TransientOperationMode.AllSolutionTimes,
            assign_strand_ids=True
        )

        logger.info(
            "Done extracting slice and setting up time strands.")

        # 4) Set up blanking
        plot.value_blanking.active = True
        # R-blanking    - always active
        self.blanking(0, "r", RelOp.LessThanOrEqual, r_threshold, active=True)

        # Bclt-blanking
        self.blanking(1, "Bclt", RelOp.LessThan, Bclt_threshold, active=False)
        self.blanking(2, "Bclt", RelOp.GreaterThan, -
                      Bclt_threshold, active=False)

        if doPlus:
            ### + side ###
            # 5) Integrate
            self.performIntegration(
                "Bclt", "Flux (+)", blanking_enable=[1], blanking_disable=[2])
            logger.debug("Done integrating + side.")

            # 6) Save images
            tp.macro.execute_command(
                """$!FrameControl ActivateByNumber Frame = 2""")
            self.twoD_plot_fix_axes(
                'C:\\Users\\yarri\\local_thesis\\scratch_11_4\\python scripts\\tecplot-files\\flux_plot_frame.sty')

            tp.export.save_png(os.path.join(self.store_gfx_path, "flux",
                                            self.run_name + "-flux-Bclt-plus.png"),
                               width=1200,
                               region=ExportRegion.CurrentFrame,
                               supersample=3,
                               convert_to_256_colors=False)
            # tp.active_page().delete_frame(tp.active_page().frames()[-1])
            logger.debug("Done saving graph + side.")

            # 7) Save data
            tp.macro.execute_extended_command(
                command_processor_id="CFDAnalyzer4",
                command=f"""SaveIntegrationResults 
                    FileName='{double_slashes(self.store_data_path)}\\\\flux\\\\{self.run_name}-flux-Bclt-plus.txt'""",
            )
            logger.debug("Done saving data + side.")
            logger.info("Done with + side.")

        if doMinus:
            tp.macro.execute_command(
                '''$!FrameControl ActivateByNumber Frame = 1''')

            ### - side ###
            self.performIntegration("Bclt", "Flux (+)", blanking_enable=[
                                    2], blanking_disable=[1])

            logger.debug("Done integrating - side.")

            # 6) Save images
            tp.macro.execute_command(
                """$!FrameControl ActivateByNumber Frame = 2"""
            )
            self.twoD_plot_fix_axes(
                'C:\\Users\\yarri\\local_thesis\\scratch_11_4\\python scripts\\tecplot-files\\flux_plot_frame.sty')

            tp.export.save_png(os.path.join(self.store_gfx_path, "flux",
                                            self.run_name + "-flux-Bclt-minus.png"),
                               width=1200,
                               region=ExportRegion.CurrentFrame,
                               supersample=3,
                               convert_to_256_colors=False)
            # tp.active_page().delete_frame(tp.active_page().frames()[-1])
            logger.debug("Done saving graph - side.")

            # 7) Save data
            tp.macro.execute_extended_command(
                command_processor_id="CFDAnalyzer4",
                command=f"""SaveIntegrationResults 
                    FileName='{double_slashes(self.store_data_path)}\\\\flux\\\\{self.run_name}-flux-Bclt-minus.txt'""",
            )
            logger.debug("Done saving data - side.")
            logger.info("Done with - side.")

    def calcFlux_Toroidal(self, Blon_threshold=B_LON_THRESHOLD, doPlus=True, doMinus=True):
        """Calculates meridional magnetic flux.
        Does the integration of both sides and saves the data.
        Similar methodology to calcFlux.
        """
        logger = self.log.getChild("fluxCalc_Toroidal")
        logger.setLevel = logging.DEBUG
        tp.macro.execute_command(
            '''$!FrameControl ActivateByNumber Frame = 1''')
        plot = tp.active_frame().plot()

        # 1) Set up slice
        plot.slice(0).orientation = SliceSurface.YPlanes
        plot.slice(0).origin.y = 0

        # 2) Extract equatorial plane slice for every time step
        # 3) Set up time strands
        self.timestrands.append("slices_at_meridional")
        plot.slices(0).extract(
            transient_mode=TransientOperationMode.AllSolutionTimes,
            assign_strand_ids=True
        )

        logger.info(
            "Done extracting slice and setting up time strands.")

        # 4) Set up blanking
        plot.value_blanking.active = True
        self.blanking(1, "Blon", RelOp.LessThan, Blon_threshold, active=False)
        self.blanking(2, "Blon", RelOp.GreaterThan, -
                      Blon_threshold, active=False)

        if doPlus:
            ### + side ###
            # 5) Integrate
            self.performIntegration(
                "Blon", "Flux (+)", blanking_enable=[1], blanking_disable=[2])
            logger.debug("Done integrating + side.")

            # 6) Save images
            tp.macro.execute_command(
                """$!FrameControl ActivateByNumber Frame = 2""")
            self.twoD_plot_fix_axes(
                'C:\\Users\\yarri\\local_thesis\\scratch_11_4\\python scripts\\tecplot-files\\flux_plot_frame.sty')

            tp.export.save_png(os.path.join(self.store_gfx_path, "flux",
                                            self.run_name + "-flux-Blon-plus.png"),
                               width=1200,
                               region=ExportRegion.CurrentFrame,
                               supersample=3,
                               convert_to_256_colors=False)
            # tp.active_page().delete_frame(tp.active_page().frames()[-1])
            logger.debug("Done saving graph + side.")

            # 7) Save data
            tp.macro.execute_extended_command(
                command_processor_id="CFDAnalyzer4",
                command=f"""SaveIntegrationResults 
                    FileName='{double_slashes(self.store_data_path)}\\\\flux\\\\{self.run_name}-flux-Blon-plus.txt'""",
            )
            logger.debug("Done saving data + side.")
            logger.info("Done with + side.")

        if doMinus:
            tp.macro.execute_command(
                '''$!FrameControl ActivateByNumber Frame = 1''')

            ### - side ###
            self.performIntegration("Blon", "Flux (-)", blanking_enable=[
                                    2], blanking_disable=[1])
            logger.debug("Done integrating - side.")

            # 6) Save images
            tp.macro.execute_command(
                """$!FrameControl ActivateByNumber Frame = 2"""
            )
            self.twoD_plot_fix_axes(
                'C:\\Users\\yarri\\local_thesis\\scratch_11_4\\python scripts\\tecplot-files\\flux_plot_frame.sty')

            tp.export.save_png(os.path.join(self.store_gfx_path, "flux",
                                            self.run_name + "-flux-Blon-minus.png"),
                               width=1200,
                               region=ExportRegion.CurrentFrame,
                               supersample=3,
                               convert_to_256_colors=False)
            # tp.active_page().delete_frame(tp.active_page().frames()[-1])
            logger.debug("Done saving graph - side.")

            # 7) Save data
            tp.macro.execute_extended_command(
                command_processor_id="CFDAnalyzer4",
                command=f"""SaveIntegrationResults 
                    FileName='{double_slashes(self.store_data_path)}\\\\flux\\\\{self.run_name}-flux-Blon-minus.txt'""",
            )
            logger.debug("Done saving data - side.")
            logger.info("Done with - side.")


if __name__ == "__main__":
    logging.basicConfig(
        filename="C:\\Users\\yarri\\local_thesis\\scratch_11_4\\python scripts\\info.log", level=logging.DEBUG)

    root_path = os.path.join(os.path.expanduser(
        "~"), "local_thesis", "scratch_11_4")
    euhforia_events_path = os.path.join(
        root_path, "euhforia_events")

    for run_name in ALL_FOLDERS:
        run_path = os.path.join(euhforia_events_path, run_name, "dat")
        run = Euhforia_Run(run_path, run_name+"debug", data_path_from_root(
            root_path), gfx_path_from_root(root_path), max_size=3)
        break
        run.calcFlux_Toroidal(5, doPlus=True, doMinus=False)
