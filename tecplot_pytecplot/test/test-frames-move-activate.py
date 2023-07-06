import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()

tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 1''')
tp.macro.execute_command('''$!FrameControl MoveToBottomByNumber
  Frame = 1''')
tp.macro.execute_command('''$!FrameControl MoveToTopByNumber
  Frame = 1''')
tp.macro.execute_command('''$!FrameControl MoveToBottomByNumber
  Frame = 3''')
# End Macro.

