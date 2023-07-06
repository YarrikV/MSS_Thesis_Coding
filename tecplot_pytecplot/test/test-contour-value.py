import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()

tp.active_frame().plot().slice(0).contour.flood_contour_group_index=1
tp.active_frame().plot().slice(0).contour.flood_contour_group_index=2
tp.active_frame().plot().slice(0).contour.flood_contour_group_index=0
tp.active_frame().plot().contour(2).variable_index=8
tp.active_frame().plot().contour(0).variable_index=4
tp.active_frame().plot().contour(1).variable_index=2
tp.active_frame().plot().contour(1).variable_index=1
tp.macro.execute_command('$!RedrawAll')
tp.active_frame().plot().contour(0).variable_index=10
# End Macro.

