import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()

tp.active_frame().plot().view.fit(consider_blanking=True)
tp.macro.execute_command('$!RedrawAll')

tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 2''')


tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 2''')


tp.active_frame().plot().frame.position = (0,
                                           tp.active_frame().plot().frame.position[1])
tp.active_frame().plot().frame.width = 3.5
tp.active_frame().plot().frame.position = (tp.active_frame().plot().frame.position[0],
                                           0)
tp.active_frame().plot().frame.height = 2
tp.active_frame().plot().frame.show_border = True
tp.active_frame().plot().frame.show_border = False
tp.active_frame().plot().frame.transparent = False
tp.active_frame().plot().frame.transparent = True
tp.macro.execute_command('$!RedrawAll')


tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 2''')

tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 2''')

tp.active_frame().plot().frame.position = (1.75,
                                           tp.active_frame().plot().frame.position[1])
tp.macro.execute_command('$!RedrawAll')

tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 2''')

tp.active_frame().plot().frame.position = (1,
                                           tp.active_frame().plot().frame.position[1])
tp.macro.execute_command('$!RedrawAll')

tp.active_frame().plot().frame.position = (tp.active_frame().plot().frame.position[0],
                                           1)
tp.macro.execute_command('$!RedrawAll')

tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 2''')

tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 2''')

tp.active_frame().plot().frame.position = (tp.active_frame().plot().frame.position[0],
                                           0)
tp.macro.execute_command('$!RedrawAll')

tp.active_frame().plot().frame.position = (1,
                                           tp.active_frame().plot().frame.position[1])
tp.active_frame().plot().frame.position = (tp.active_frame().plot().frame.position[0],
                                           0.5)
tp.macro.execute_command('$!RedrawAll')

tp.macro.execute_command('$!RedrawAll')

tp.active_frame().plot().frame.position = (1,
                                           tp.active_frame().plot().frame.position[1])
tp.active_frame().plot().frame.position = (tp.active_frame().plot().frame.position[0],
                                           0.25)
tp.macro.execute_command('$!RedrawAll')

tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 1''')
tp.macro.execute_command('$!RedrawAll')
tp.macro.execute_command('$!GlobalTime SolutionTime = 0')
tp.macro.execute_command('$!RedrawAll')
tp.export.save_time_animation_mpeg4('C:/Users/yarri/local_thesis/scratch_11_4/gfx/flux/movies/test-flux-anim.mp4',
                                    start_time=0,
                                    end_time=56,
                                    timestep_step=1,
                                    width=1024,
                                    animation_speed=10,
                                    region=ExportRegion.AllFrames,
                                    supersample=3)
# End Macro.
