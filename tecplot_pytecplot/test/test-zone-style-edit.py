import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()

tp.active_frame().plot().fieldmaps(1).show=False
tp.active_frame().plot().show_shade=False
tp.macro.execute_command('$!GlobalTime SolutionTime = 24')
tp.macro.execute_command('$!RedrawAll')
tp.active_frame().plot().show_shade=True
tp.macro.execute_command('$!GlobalTime SolutionTime = 23')
tp.macro.execute_command('$!GlobalTime SolutionTime = 22')
tp.macro.execute_command('$!GlobalTime SolutionTime = 21')
tp.macro.execute_command('$!GlobalTime SolutionTime = 20')
tp.macro.execute_command('$!RedrawAll')
tp.active_frame().plot().fieldmaps(1).show=True
# End Macro.

