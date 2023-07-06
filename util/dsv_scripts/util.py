
import glob
import datetime
import os.path
import argparse
from datetime import datetime
# import configparser

import numpy as np
import scipy as sp
import scipy.constants
from astropy.constants import au, R_sun

# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator, AutoLocator
from matplotlib.dates import DayLocator, HourLocator, DateFormatter
from matplotlib.font_manager import FontProperties
import matplotlib.dates as mdates

import csv
from math import *
import pandas as pd

import os
import sys
print(sys.argv)


def phi_y_by_l(tstart, tend, By, Vx, t):  # This is the azimuthal phi
    '''
    Direct method to estimate the accumulated azimuthal magnetic flux per unit length, Pal et al., 2021.
    V(x,FR) represents the FR speed in the direction of x(FR) and L is the length of the FR.'''
    phiy_over_l = []
    vx_max = np.max(Vx)
    # Vx*1e3 = [m/s]; By*1e-9 = [T]; Multiplied with 1e8 to convert into Mx; Divided by 1 au
    phiy_over_l = [By[i]*1e-9*vx_max*1e3*1e8 *
                   au.value for i in range(tstart, tend)]
    # replacing Vx[i] with vx_max to see how erosion estimation is affected.

    return phiy_over_l


def draw_vertical(euhforia_earth_beta, t, ax):
    k_end = 0
    k_beg = 0
    t_beg = []
    t_end = []
    t_all = []
    indices = []
    thrs = 0.1
    for kk in range(len(euhforia_earth_beta)-1):
        # and k>0:
        if ((euhforia_earth_beta[kk] < thrs and euhforia_earth_beta[kk-1] > thrs)) or ((euhforia_earth_beta[kk] < thrs and euhforia_earth_beta[kk+1] > thrs)):
            k_end = +1  # k_end odd
            t_all.append(t[kk])
            indices.append(kk)

    for i in range(len(t_all)-1):
        # if i == 0:
        #    ax.axvspan(t_all[i], t_all[i+1], alpha=0.2, color='green')

        if i == 2:
            ax.axvspan(t_all[i], t_all[i+1], alpha=0.2, color='blue')

        i = +1

    # These are the start  and end times of the MC
    return (t_all[-2], t_all[-1], indices[-2], indices[-1])


def draw_shock(euhforia_earth_v):
    # for ind in range(len(euhforia_earth_v_spr)-12):
    for ind in range(1, len(euhforia_earth_v)-1):
        # and euhforia_earth_v_spr[ind+10]>euhforia_earth_v_spr[ind]: 1. 15; 2.
        if 100*(euhforia_earth_v[ind-1] - euhforia_earth_v[ind])/euhforia_earth_v[ind] > 15:
            print(i, ' : ', r[ind], euhforia_earth_v[ind])
            plt.axvline(x=r[ind], c='y', linestyle='-', linewidth=lw)


def find_mc_centre(euhforia_earth_by_spr, t, ax):
    '''
    Finds the centre of the MC when By changes sign
    '''
    by = euhforia_earth_by_spr
    turns = 0
    ctr = []

    for i in range(1, len(by)):
        if turns < 2:  # The profile changes sign twice - once at the front and then at the middle
            if np.sign(by[i]) == -np.sign(by[i-1]):
                ctr.append(i)
                turns = +1

    #ax.axvline(x=t[ctr[0]],c='y',linestyle='-', linewidth=lw)
    return ctr[1]
