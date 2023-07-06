import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()

tp.active_frame().plot().slice(0).obey_source_zone_blanking=False
tp.active_frame().plot().slice(0).obey_source_zone_blanking=True
tp.active_frame().plot().slice(0).obey_source_zone_blanking=False
tp.active_frame().plot().slice(0).obey_source_zone_blanking=True
# End Macro.

