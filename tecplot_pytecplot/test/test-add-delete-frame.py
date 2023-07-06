import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()

tp.macro.execute_command('''$!FrameControl DeleteByNumber
  Frame = 2''')
tp.active_page().add_frame(position=(1.4374,1.7086),
    size=(1.226,1.5928))
# End Macro.

