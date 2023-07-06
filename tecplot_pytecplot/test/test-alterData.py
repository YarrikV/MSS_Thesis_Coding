import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()

tp.data.operate.execute_equation(equation='{bz_eq}=-{bclt}',
    ignore_divide_by_zero=True)
tp.data.operate.execute_equation(equation='{bz_above_or_below}=IF({bz_eq}>5,1,IF({bz_eq}<-5,1,0))',
    ignore_divide_by_zero=True)
# End Macro.

