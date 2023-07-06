import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()


tp.active_frame().plot().contour(0).legend.box.box_type = tp.constant.TextBox.Filled
tp.macro.execute_command('$!RedrawAll')

tp.active_frame().plot().contour(0).legend.box.box_type = tp.constant.TextBox.None_
tp.macro.execute_command('$!RedrawAll')
# End Macro.
