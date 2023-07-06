import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()

tp.macro.execute_extended_command(command_processor_id='CFDAnalyzer4',
                                  command="Integrate [1-57] VariableOption='Scalar' XOrigin=0 YOrigin=0 ZOrigin=0 ScalarVar=10 Absolute='F' ExcludeBlanked='F' XVariable=1 YVariable=2 ZVariable=3 IntegrateOver='Cells' IntegrateBy='Zones' IRange={MIN =1 MAX = 0 SKIP = 1} JRange={MIN =1 MAX = 0 SKIP = 1} KRange={MIN =1 MAX = 0 SKIP = 1} PlotResults='T' PlotAs='Flux' TimeMin=0 TimeMax=56")


tp.macro.execute_extended_command(command_processor_id='CFDAnalyzer4',
                                  command="Integrate [57] VariableOption='Scalar' XOrigin=0 YOrigin=0 ZOrigin=0 ScalarVar=10 Absolute='F' ExcludeBlanked='F' XVariable=1 YVariable=2 ZVariable=3 IntegrateOver='Cells' IntegrateBy='TimeStrands' IRange={MIN =1 MAX = 0 SKIP = 1} JRange={MIN =1 MAX = 0 SKIP = 1} KRange={MIN =1 MAX = 0 SKIP = 1} PlotResults='T' PlotAs='Flux' TimeMin=0 TimeMax=56")
tp.macro.execute_command('$!GlobalTime SolutionTime = 31')
tp.macro.execute_command('$!GlobalTime SolutionTime = 0')

#  Recording canceled
