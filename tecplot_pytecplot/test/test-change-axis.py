import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()


tp.active_frame().plot().frame.width = 6


tp.active_frame().plot().axes.y_axis(
    0).tick_labels.alignment = LabelAlignment.AlongAxis

tp.active_frame().plot().axes.y_axis(
    0).tick_labels.alignment = LabelAlignment.PerpendicularToAxis

tp.active_frame().plot().axes.y_axis(
    0).tick_labels.alignment = LabelAlignment.AlongAxis

tp.active_frame().plot().axes.y_axis(0).fit_range()
tp.active_frame().plot().axes.x_axis(0).fit_range()
tp.active_frame().plot().axes.x_axis(0).max = 60
tp.macro.execute_command('$!RedrawAll')
# End Macro.
