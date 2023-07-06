import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()

tp.active_frame().plot().slice(0).orientation=SliceSurface.XPlanes
tp.active_frame().plot().slice(0).orientation=SliceSurface.YPlanes
tp.active_frame().plot().slice(0).contour.flood_contour_group_index=1
tp.active_frame().plot().slice(0).contour.flood_contour_group_index=0
tp.active_frame().plot().slices(0).extract(transient_mode=TransientOperationMode.AllSolutionTimes)
tp.macro.execute_extended_command(command_processor_id='Strand Editor',
    command='ZoneSet=58-114;AssignStrands=TRUE;StrandValue=2;AssignSolutionTime=TRUE;TimeValue=0;DeltaValue=1;TimeOption=ConstantDelta;')
tp.macro.execute_extended_command(command_processor_id='CFDAnalyzer4',
    command="Integrate [2] VariableOption='Scalar' XOrigin=0 YOrigin=0 ZOrigin=0 ScalarVar=11 Absolute='F' ExcludeBlanked='F' XVariable=1 YVariable=2 ZVariable=3 IntegrateOver='Cells' IntegrateBy='TimeStrands' IRange={MIN =1 MAX = 0 SKIP = 1} JRange={MIN =1 MAX = 0 SKIP = 1} KRange={MIN =1 MAX = 0 SKIP = 1} PlotResults='T' PlotAs='Toroidal flux (Total)' TimeMin=0 TimeMax=56")
tp.active_frame().plot().show_shade=False
tp.active_frame().plot().show_shade=True
tp.active_frame().plot().show_shade=False
# End Macro.

