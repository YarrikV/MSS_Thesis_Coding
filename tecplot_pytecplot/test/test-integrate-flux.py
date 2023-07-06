import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# extract slice 0
tp.active_frame().plot().slices(0).extract(
    transient_mode=TransientOperationMode.AllSolutionTimes)

#                                                  | this is which blanking number
tp.active_frame().plot().value_blanking.constraint(0).comparison_value = 0.12

# activate all blanking
tp.active_frame().plot().value_blanking.active = True

# activate specific blanking, e.g. blanking nr 0 (first one)
tp.active_frame().plot().value_blanking.constraint(0).active = True

# change variable of specific (1) blanking
tp.active_frame().plot().value_blanking.constraint(1).variable_index = 9

# ? maybe also possible
# ? > ....constraint(1).variable = dataset.variable('S')

# change operator and comparison value of specific blanking
tp.active_frame().plot().value_blanking.constraint(
    1).comparison_operator = RelOp.LessThan
tp.active_frame().plot().value_blanking.constraint(1).comparison_value = 2


# blank r
tp.active_frame().plot().value_blanking.constraint(0).active = True
tp.active_frame().plot().value_blanking.constraint(0).comparison_value = 0.12

# blank Bclt less than 2
tp.active_frame().plot().value_blanking.constraint(1).active = True
tp.active_frame().plot().value_blanking.constraint(1).variable_index = 9
tp.active_frame().plot().value_blanking.constraint(
    1).comparison_operator = RelOp.LessThan
tp.active_frame().plot().value_blanking.constraint(1).comparison_value = 2

# blank Bclt greater than -5
tp.active_frame().plot().value_blanking.constraint(2).variable_index = 9
tp.active_frame().plot().value_blanking.constraint(
    2).comparison_operator = RelOp.GreaterThan
tp.active_frame().plot().value_blanking.constraint(2).comparison_value = -5
tp.active_frame().plot().value_blanking.constraint(2).active = True

# set strands for extracted slices
tp.macro.execute_extended_command(command_processor_id='Strand Editor',
                                  command='ZoneSet=57,1-56;AssignStrands=TRUE;StrandValue=57;AssignSolutionTime=TRUE;TimeValue=0;DeltaValue=1;TimeOption=ConstantDelta;')
tp.macro.execute_extended_command(command_processor_id='Strand Editor',
                                  command='ZoneSet=58-114;AssignStrands=TRUE;StrandValue=57;AssignSolutionTime=TRUE;TimeValue=0;DeltaValue=1;TimeOption=ConstantDelta;')
tp.macro.execute_extended_command(command_processor_id='Strand Editor',
                                  command='ZoneSet=114,58-113;AssignStrands=TRUE;StrandValue=1;AssignSolutionTime=TRUE;TimeValue=0;DeltaValue=1;TimeOption=ConstantDelta;')
tp.macro.execute_extended_command(command_processor_id='Strand Editor',
                                  command='ZoneSet=57,1-56;AssignStrands=TRUE;StrandValue=0;AssignSolutionTime=TRUE;TimeValue=0;DeltaValue=1;TimeOption=ConstantDelta;')
tp.macro.execute_extended_command(command_processor_id='CFDAnalyzer4',
                                  command="Integrate [1] VariableOption='Scalar' XOrigin=0 YOrigin=0 ZOrigin=0 ScalarVar=10 Absolute='F' ExcludeBlanked='T' XVariable=1 YVariable=2 ZVariable=3 IntegrateOver='Cells' IntegrateBy='TimeStrands' IRange={MIN =1 MAX = 0 SKIP = 1} JRange={MIN =1 MAX = 0 SKIP = 1} KRange={MIN =1 MAX = 0 SKIP = 1} PlotResults='T' PlotAs='Flux (+ side)' TimeMin=0 TimeMax=56")
tp.macro.execute_extended_command(command_processor_id='CFDAnalyzer4',
                                  command="SaveIntegrationResults FileName='C:\\\\Users\\\\yarri\\\\local_thesis\\\\scratch_11_4\\\\data\\\\test-flux.txt'")

tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 1''')
tp.macro.execute_command('$!GlobalTime SolutionTime = 0')
tp.macro.execute_command('$!RedrawAll')

tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 2''')
tp.active_frame().load_stylesheet(
    'C:\\Users\\yarri\\local_thesis\\scratch_11_4\\tecplot-relativedensity\\mass_plot_frame.sty')
tp.macro.execute_command('$!RedrawAll')

tp.active_frame().plot().axes.x_axis(0).min = 0
tp.active_frame().plot().axes.x_axis(0).max = 60
tp.active_frame().plot().axes.y_axis(0).fit_range()
tp.macro.execute_command('$!RedrawAll')

tp.active_frame().load_stylesheet(
    'C:\\Users\\yarri\\local_thesis\\scratch_11_4\\tecplot-relativedensity\\flux_plot_frame.sty')

tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 2''')
tp.macro.execute_command('$!RedrawAll')
tp.export.save_png('C:\\Users\\yarri\\local_thesis\\scratch_11_4\\gfx\\flux\\test-flux.png',
                   width=1200,
                   region=ExportRegion.CurrentFrame,
                   supersample=3,
                   convert_to_256_colors=False)
# End Macro.
