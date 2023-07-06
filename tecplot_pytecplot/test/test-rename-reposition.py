import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()

tp.active_frame().plot().value_blanking.constraint(1).variable_index = 0
tp.active_frame().plot().value_blanking.constraint(
    1).comparison_variable_index = 0

tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 2''')
tp.active_frame().name = 'test-1-2'

tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 3''')
tp.active_frame().load_stylesheet(
    'C:\\Users\\yarri\\local_thesis\\scratch_11_4\\python scripts\\tecplot-files\\flux_visuals_2.sty')

tp.macro.execute_command('$!RedrawAll')

tp.active_frame().plot().value_blanking.constraint(1).variable_index = 0
tp.active_frame().plot().value_blanking.constraint(
    1).comparison_variable_index = 0
tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 3''')


tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 2''')

tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 3''')


tp.active_frame().plot().frame.position = (1, 0.25)
tp.active_frame().plot().frame.width = 3.5

tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 2''')

tp.active_frame().plot().frame.position = (1, 2.25)
tp.active_frame().name = 'test-2-3'
tp.active_frame().load_stylesheet(
    'C:\\Users\\yarri\\local_thesis\\scratch_11_4\\python scripts\\tecplot-files\\flux_visuals_2.sty')
# End Macro.
