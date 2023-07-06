import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()
tp.active_frame().plot().frame.show_border = False
tp.active_frame().plot().slice(0).contour.flood_contour_group_index = 1
tp.active_frame().plot().slice(0).contour.flood_contour_group_index = 0
tp.active_frame().plot().contour(0).variable_index = 11
tp.active_frame().plot().contour(0).variable_index = 15
tp.active_frame().plot().contour(0).levels.reset_levels([-5, 5])
tp.macro.execute_command('$!RedrawAll')
# End Macro.
