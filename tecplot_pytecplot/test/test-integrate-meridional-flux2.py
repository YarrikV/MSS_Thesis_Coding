import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()

tp.active_frame().plot().value_blanking.active = False
tp.active_frame().plot().value_blanking.active = True
tp.active_frame().plot().value_blanking.constraint(0).active = False
tp.active_frame().plot().value_blanking.constraint(0).active = True
tp.active_frame().plot().value_blanking.cell_mode = ValueBlankCellMode.AnyCorner
tp.active_frame().plot().value_blanking.cell_mode = ValueBlankCellMode.AllCorners
tp.active_frame().plot().value_blanking.constraint(2).variable_index = 0
tp.active_frame().plot().value_blanking.constraint(0).variable_index = 4
tp.active_frame().plot().value_blanking.constraint(0).variable_index = 11
tp.active_frame().plot().value_blanking.constraint(0).variable_index = 10
tp.active_frame().plot().value_blanking.constraint(
    0).comparison_operator = RelOp.GreaterThanOrEqual
tp.active_frame().plot().value_blanking.constraint(
    0).comparison_operator = RelOp.GreaterThan
tp.active_frame().plot().value_blanking.constraint(
    0).comparison_operator = RelOp.LessThan
tp.active_frame().plot().value_blanking.constraint(0).active = False
tp.active_frame().plot().value_blanking.constraint(0).active = True
tp.macro.execute_extended_command(command_processor_id='CFDAnalyzer4',
                                  command="Integrate [2] VariableOption='Scalar' XOrigin=0 YOrigin=0 ZOrigin=0 ScalarVar=11 Absolute='F' ExcludeBlanked='T' XVariable=1 YVariable=2 ZVariable=3 IntegrateOver='Cells' IntegrateBy='TimeStrands' IRange={MIN =1 MAX = 0 SKIP = 1} JRange={MIN =1 MAX = 0 SKIP = 1} KRange={MIN =1 MAX = 0 SKIP = 1} PlotResults='T' PlotAs='Toroidal flux (+)' TimeMin=0 TimeMax=56")
tp.macro.execute_extended_command(command_processor_id='CFDAnalyzer4',
                                  command="SaveIntegrationResults FileName='C:\\\\Users\\\\yarri\\\\local_thesis\\\\scratch_11_4\\\\data\\\\flux-merid\\\\temp.txt'")

tp.active_frame().load_stylesheet(
    'C:\\Users\\yarri\\local_thesis\\scratch_11_4\\tecplot-relativedensity\\flux_plot_frame.sty')

tp.active_frame().plot().axes.y_axis(0).fit_range()

tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 2''')

tp.macro.execute_command('$!RedrawAll')
tp.export.save_png('C:\\Users\\yarri\\local_thesis\\scratch_11_4\\gfx\\flux-meridional\\TEMP.png',
                   width=1024,
                   region=ExportRegion.CurrentFrame,
                   supersample=3,
                   convert_to_256_colors=False)
# End Macro.
