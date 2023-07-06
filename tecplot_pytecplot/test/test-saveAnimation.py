import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()


tp.active_frame().plot().contour(0).legend.box.box_type = tp.constant.TextBox.None_

tp.active_frame().plot().view.psi = 50
tp.active_frame().plot().view.position = (
    0.128104,
    tp.active_frame().plot().view.position[1],
    tp.active_frame().plot().view.position[2],
)
tp.active_frame().plot().view.position = (
    tp.active_frame().plot().view.position[0],
    -22.7336,
    tp.active_frame().plot().view.position[2],
)
tp.active_frame().plot().view.position = (
    tp.active_frame().plot().view.position[0],
    tp.active_frame().plot().view.position[1],
    19.2618,
)
tp.active_frame().plot().view.width = 4


tp.active_frame().plot().slice(0).effects.use_translucency = True
tp.active_frame().plot().slice(0).effects.surface_translucency = 30
tp.macro.execute_command("$!RedrawAll")

tp.export.save_time_animation_mpeg4(
    "D:\\local-thesis\\gfx\\mass111-test.mp4",
    start_time=0,
    end_time=3,
    timestep_step=1,
    width=841,
    animation_speed=10,
    region=ExportRegion.CurrentFrame,
    supersample=3,
)
# End Macro.
