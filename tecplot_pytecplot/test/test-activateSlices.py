import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()

tp.active_frame().plot(PlotType.Cartesian3D).show_slices=False
tp.active_frame().plot(PlotType.Cartesian3D).show_slices=True
tp.active_frame().plot().slice(0).show=False
tp.active_frame().plot().slice(0).show=True
tp.active_frame().plot().slice(1).show=False
tp.active_frame().plot().slice(1).show=True
# End Macro.

