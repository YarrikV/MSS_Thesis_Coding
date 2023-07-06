import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()
# XYZ VIEW
tp.active_frame().plot().view.position = (15.2473, 8.80301, 10.1648)
tp.active_frame().plot().view.psi = 60
tp.active_frame().plot().view.theta = 240
tp.macro.execute_command('$!RedrawAll')

# ZY VIEW
tp.active_frame().plot().view.position = (20.3297, 0, 0)

# ZX VIEW
tp.active_frame().plot().view.psi = 90
tp.active_frame().plot().view.theta = -90
tp.active_frame().plot().view.position = (0, 0, 0)

# XY VIEW
tp.active_frame().plot().view.position = (0, -20.3297, 0)
tp.active_frame().plot().view.theta = 0
tp.active_frame().plot().view.position = (0, 0, 20.3297)
tp.active_frame().plot().view.psi = 0
tp.macro.execute_command('$!RedrawAll')
# End Macro.
