import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()


tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 3''')
tp.active_frame().plot().frame.transparent = True
tp.macro.execute_command('$!RedrawAll')
# End Macro.
