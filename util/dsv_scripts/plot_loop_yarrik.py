
#!/usr/bin/env python

"""
Plots 
all magnetic field components and total magnetic field
for multiple EUHFORIA time series along with OMNI data.
"""
from util import *
from tqdm import tqdm

all_folders = [
    "mass111",
    "mass112",
    # "mass113",
    # "mass121",
    # "mass122",
    "mass123",
    "mass131",
    "mass132",
    "mass133",
    "mass211",
    "mass212",
    "mass213",
    "mass221",
    "mass222",
    "mass223",
    "mass231",
    "mass232",
    "mass233",
    "mass311",
    "mass312",
    "mass313",
    "mass321",
    "mass322",
    "mass323",
    "mass331",
    "mass332",
    "mass333",
]

for run_name in tqdm(all_folders):

    # name of the run
    #run_name = 'mass111'

    # VSC you want to look at
    loc = 'Earth'  # 'SC016' #R4_14' #

    # ?
    # pos_label = 'r = 0.4 au, lon = 45$^0$'
    # pos_save = 'r0p4_lon45'

    # ?
    date_beg = "2012-07-12T00:00:00"
    date_end = "2012-07-20T00:00:00"

    # directory where data are stored
    # ???
    data_dir = os.path.join("..", "euhforia_events", run_name, run_name)
    t7 = data_dir  # os.path.join("..", "data", run_name, run_name)

    png_name = "timeseries_" + run_name + "_" + loc     # output file name

    dsv = [t7]
    infile = [loc]

    lbl = [run_name]        # label of legend of P plot
    suptitle = run_name     # title of figure

    # directory where plots will be stored
    output_dir = os.path.join("..", "gfx", "timeseries", "")

    # PLOTTING CONSTANTS
    color = ['b-', 'r-', 'm-', 'g-', 'k-', 'c-', 'b--', 'r--', 'm--']
    alpha = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5]
    lw = [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2]
    ytic_size = 12
    xtic_size = 10
    ylab_font = 12
    xlab_font = 12

    # PHYSICAL CONSTANTS
    mu_0 = 4*np.pi*(10**(-7.))  # vacuum magnetic permeability [SI: N / A^2]
    mu = 1              # mean molecular weight of the plasma
    m_p = 1.6726 * (10**(-27.))     # proton mass [kg]
    kB = scipy.constants.k

    # TIMING
    yr = date_beg[:4]
    dd = date_beg[:4] + date_beg[5:7] + date_beg[8:10]

    # time interval you want to plot
    start_date = datetime.strptime(
        date_beg, "%Y-%m-%dT%H:%M:%S")  # 2020-05-14T02:00:00
    end_date = datetime.strptime(
        date_end, "%Y-%m-%dT%H:%M:%S")  # 2020-05-17T00:00:00

    #------------------------------------------------------------------------#
    #------------------------------- OMNI Data ------------------------------#
    #------------------------------------------------------------------------#

    #omni_dir = '/home/u0141347/kul/EUHFORIA/runs/'+dd+'/'
    #omni_file = 'omni_5min_20120712-20120718.lst' #'omni_min_20130411-20130421.lst' #

    fig = plt.figure(figsize=(14, 14), dpi=80)
    # --------------------------------------------------------
    # READING IN EUHFORIA DATA
    # --------------------------------------------------------
    num = 0

    bmax = []
    bzmin = []
    vmax = []

    for i in dsv:

        date = '20120712'

        # directory where data are stored
        data_dir_spr = i

        # --------------------------------------------------------
        # READING IN EUHFORIA DATA
        # --------------------------------------------------------

        file_spr = []
        # input files from EUHFORIA
        file_spr.append(i + "_" + infile[num] + ".dsv")

        print("Files loaded:")

        print(file_spr)

        # column format in euhforia data file
        data_earth_spr = np.loadtxt(file_spr[0], delimiter=' ', skiprows=1, usecols=[
                                    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        print("amount of time steps:", len(data_earth_spr))

        # dates
        date_earth1 = np.loadtxt(
            file_spr[0], delimiter=' ', dtype='str', skiprows=1, usecols=[0])

        # assigning date to euhforia data
        final_dates1 = []
        for dates in date_earth1:
            final_dates1.append(datetime.strptime(
                str(dates), "%Y-%m-%dT%H:%M:%S"))
        '''
        kp_date = np.loadtxt(i+'/kp.dat', delimiter=' ', dtype='str', skiprows=1, usecols=[0])
        kp = np.loadtxt(i+'/kp.dat', delimiter=' ', skiprows=1, usecols=[1]) #kp_date = kp_dates[0]; 
        kp_dates1 = []
        for date in kp_date:
            kp_dates1.append( datetime.strptime(str(date), "%Y-%m-%dT%H:%M:%S") )
        '''
        # ================================================================================================
        # DEFINING VARIABLES
        # ================================================================================================

        # defining V and B
        euhforia_earth_v_spr = np.sqrt(
            data_earth_spr[:, 5]**2 + data_earth_spr[:, 6]**2 + data_earth_spr[:, 7]**2)
        euhforia_earth_b_spr = np.sqrt(
            data_earth_spr[:, 8]**2 + data_earth_spr[:, 9]**2 + data_earth_spr[:, 10]**2)

        euhforia_earth_vx_spr = -data_earth_spr[:, 5]  # = - v_r
        euhforia_earth_vy_spr = -data_earth_spr[:, 7]  # = - v_lon
        euhforia_earth_vz_spr = -data_earth_spr[:, 6]  # = - v_clt

        euhforia_earth_bx_spr = -data_earth_spr[:, 8]  # = - b_r
        euhforia_earth_by_spr = -data_earth_spr[:, 10]  # = - b_lon
        euhforia_earth_bz_spr = -data_earth_spr[:, 9]  # = - b_clt

        # defining pressures
        euhforia_earth_p_therm_spr = data_earth_spr[:, 4]  # [Pa]
        euhforia_earth_p_mag_spr = (
            (euhforia_earth_b_spr*10**-9.0)**2.0)/(2.0*(10**-7))
        euhforia_earth_p_int_spr = euhforia_earth_p_therm_spr + euhforia_earth_p_mag_spr

        euhforia_earth_beta_spr = euhforia_earth_p_therm_spr/euhforia_earth_p_mag_spr

        # defining number density
        euhforia_earth_n_spr = 0.5*data_earth_spr[:, 3]
        euhforia_earth_p_dyn_spr = euhforia_earth_n_spr*1e6 * \
            m_p*euhforia_earth_v_spr*euhforia_earth_v_spr*1e6

        # =================================================================================================
        # MAKING PLOTSinfile
        # =================================================================================================

        print("Making nice plots...")

        label1 = lbl[num]  # 'SC_'+str(i+1)
        font = FontProperties()
        font.set_family('serif')
        font.set_name('Times New Roman')

        # --------------------------------
        # V
        # --------------------------------

        axis = plt.subplot(8, 1, 1)

        # axes range
        #axis.set_ylim((400, 800))
        axis.set_xlim((start_date, end_date))
        axis.plot(final_dates1, euhforia_earth_v_spr,
                  color[num], linewidth=lw[num],  label=label1, alpha=alpha[num])
        axis.xaxis.set_minor_locator(AutoMinorLocator(6))
        #axis.plot( [final_dates1[-1], final_dates1[-1]], [0, 1000], '-k', lw=2, alpha=0.5)
        plt.setp(axis.get_xticklabels(), visible=False)
        plt.setp(axis.get_yticklabels(), visible=True, fontsize=ytic_size)

        for ind in range(len(euhforia_earth_v_spr)-12):
            # and euhforia_earth_v_spr[ind+10]>euhforia_earth_v_spr[ind]:
            if 100*(euhforia_earth_v_spr[ind+1] - euhforia_earth_v_spr[ind])/euhforia_earth_v_spr[ind] > 5:
                print(i, ' : ', final_dates1[ind], euhforia_earth_v_spr[ind])

        # Show grid
        plt.grid()

        axis.yaxis.set_label_text(
            "$v [km/s]$", fontsize=ylab_font, fontweight='bold')
        # fig.subplots_adjust(left=left)
        plt.legend(bbox_to_anchor=(1.0, 1.0),
                   loc='upper right', prop={'size': 8}, ncol=3)

        # plt.legend(bbox_to_anchor=(0.5, 1.3),loc='center',prop={'size':12},ncol=6) #upper right
        draw_vertical(euhforia_earth_beta_spr, final_dates1, axis)

        # --------------------------------
        # n
        # --------------------------------

        axis = plt.subplot(8, 1, 2)

        # axes range
        #axis.set_ylim((ylim_low_v, ylim_up_v))
        #axis.set_ylim((0.1, 100))
        axis.set_xlim((start_date, end_date))

        axis.plot(final_dates1, euhforia_earth_n_spr,
                  color[num], linewidth=lw[num],  label=label1, alpha=alpha[num])
        axis.xaxis.set_minor_locator(AutoMinorLocator(6))
        plt.setp(axis.get_xticklabels(), visible=False)
        plt.setp(axis.get_yticklabels(), visible=True, fontsize=ytic_size)
        # plt.yscale('log')
        minor_locator = AutoMinorLocator(2)
        #major_locator = AutoLocator()
        axis.yaxis.set_minor_locator(minor_locator)
        # axis.yaxis.set_major_locator(MultipleLocator(10)) #100
        plt.axhline(y=0, ls='--', c='k', lw=0.7)

        # Show grid
        plt.grid()

        axis.yaxis.set_label_text(
            "$n [/cm^3]$", fontsize=ylab_font, fontweight='bold')
        # fig.subplots_adjust(left=left)
        draw_vertical(euhforia_earth_beta_spr, final_dates1, axis)

        # --------------------------------
        # p_therm
        # --------------------------------
        axis = plt.subplot(8, 1, 3)

        # axes range
        #axis.set_ylim((ylim_low_v, ylim_up_v))
        #axis.set_ylim((0, 2))
        axis.set_xlim((start_date, end_date))
        axis.plot(final_dates1, euhforia_earth_p_therm_spr*1e9,
                  color[num], linewidth=lw[num],  linestyle='--', label=label1+'_ptherm')
        axis.plot(final_dates1, euhforia_earth_p_dyn_spr*1e9,
                  color[num], linewidth=lw[num],  linestyle='-',  label=label1+'_pdyn')
        axis.plot(final_dates1, euhforia_earth_p_int_spr*1e9,
                  color[num], linewidth=lw[num],  linestyle='dashdot',  label=label1+'_p(mag+therm)')
        axis.xaxis.set_minor_locator(AutoMinorLocator(6))

        #axis.plot( [final_dates1[-1], final_dates1[-1]], [0, 4000], '-k', lw=2, alpha=0.5)
        plt.setp(axis.get_xticklabels(), visible=False, fontsize=7)
        plt.setp(axis.get_yticklabels(), visible=True, fontsize=ytic_size)

        # Show grid
        plt.grid()
        # Show legend
        plt.legend(loc=4, prop={'size': 8})  # (loc=2,prop={'size':8})

        #axis.yaxis.set_ticks(np.linspace(ylim_low_v, ylim_up_v, 2))
        #axis.yaxis.set_major_locator( MultipleLocator(10) )
        #axis.yaxis.set_minor_locator( MultipleLocator(10) )
        axis.yaxis.set_label_text(
            "$P [nPa]$", fontsize=ylab_font, fontweight='bold')

        draw_vertical(euhforia_earth_beta_spr, final_dates1, axis)

        # --------------------------------
        # B_x
        # --------------------------------

        axis = plt.subplot(8, 1, 4)

        # axes range
        #axis.set_ylim((-20, 20))
        axis.set_xlim((start_date, end_date))

        axis.plot(final_dates1, euhforia_earth_bx_spr,
                  color[num], linewidth=lw[num],  label=label1, alpha=alpha[num])
        axis.xaxis.set_minor_locator(AutoMinorLocator(6))
        #axis.plot( [final_dates1[-1], final_dates1[-1]], [0, 10], '-k', lw=2, alpha=0.5)
        plt.setp(axis.get_xticklabels(), visible=False)
        plt.setp(axis.get_yticklabels(), visible=True, fontsize=ytic_size)
        plt.axhline(y=0, ls='--', c='k', lw=0.7)

        # Show grid
        plt.grid()

        axis.yaxis.set_label_text(
            "$B_x [nT]$", fontsize=ylab_font, fontweight='bold')
        # fig.subplots_adjust(left=left)
        # plt.legend(bbox_to_anchor=(0.5, 1.3),loc='center',prop={'size':12},ncol=3) #upper right
        draw_vertical(euhforia_earth_beta_spr, final_dates1, axis)

        # --------------------------------
        # B_y
        # --------------------------------

        axis = plt.subplot(8, 1, 5)

        # axes range
        #axis.set_ylim((-20, 20))
        axis.set_xlim((start_date, end_date))

        axis.plot(final_dates1, euhforia_earth_by_spr,
                  color[num], linewidth=lw[num],  label=label1, alpha=alpha[num])
        axis.xaxis.set_minor_locator(AutoMinorLocator(6))
        #axis.plot( [final_dates1[-1], final_dates1[-1]], [0, 10], '-k', lw=2, alpha=0.5)
        plt.setp(axis.get_xticklabels(), visible=False)
        plt.setp(axis.get_yticklabels(), visible=True, fontsize=ytic_size)
        plt.axhline(y=0, ls='--', c='k', lw=0.7)

        # Show grid
        plt.grid()

        axis.yaxis.set_label_text(
            "$B_y [nT]$", fontsize=ylab_font, fontweight='bold')
        # fig.subplots_adjust(left=left)
        draw_vertical(euhforia_earth_beta_spr, final_dates1, axis)

        # --------------------------------
        # B_z
        # --------------------------------

        axis = plt.subplot(8, 1, 6)

        # axes range
        #axis.set_ylim((-20, 20))
        axis.set_xlim((start_date, end_date))

        axis.plot(final_dates1, euhforia_earth_bz_spr,
                  color[num], linewidth=lw[num],  label=label1, alpha=alpha[num])
        axis.xaxis.set_minor_locator(AutoMinorLocator(6))

        plt.setp(axis.get_xticklabels(), visible=False)
        plt.setp(axis.get_yticklabels(), visible=True, fontsize=ytic_size)
        plt.axhline(y=0, ls='--', c='k', lw=0.7)

        # Show grid
        plt.grid()

        axis.yaxis.set_label_text(
            "$B_z [nT]$", fontsize=ylab_font, fontweight='bold')
        # fig.subplots_adjust(left=left)
        draw_vertical(euhforia_earth_beta_spr, final_dates1, axis)

        # --------------------------------
        # B_total
        # --------------------------------

        axis = plt.subplot(8, 1, 7)

        # axes range
        #axis.set_ylim((0, 20))
        axis.set_xlim((start_date, end_date))

        axis.plot(final_dates1, euhforia_earth_b_spr,
                  color[num], linewidth=lw[num],  label=label1, alpha=alpha[num])
        axis.xaxis.set_minor_locator(AutoMinorLocator(6))

        plt.setp(axis.get_xticklabels(), visible=True)
        plt.setp(axis.get_yticklabels(), visible=True, fontsize=ytic_size)
        plt.axhline(y=0, ls='--', c='k', lw=0.7)

        # Show grid
        plt.grid()
        # Show legend
        # plt.legend(prop={'size':8})
        axis.yaxis.set_label_text(
            "$|B| [nT]$", fontsize=ylab_font, fontweight='bold')
        draw_vertical(euhforia_earth_beta_spr, final_dates1, axis)

        # --------------------------------
        # Beta
        # --------------------------------

        axis = plt.subplot(8, 1, 8)

        # axes range
        #axis.set_ylim((0.001, 100000.0)) #(0.001,10)) #
        axis.set_xlim((start_date, end_date))
        axis.plot(final_dates1, euhforia_earth_beta_spr,
                  color[num], linewidth=lw[num],  label=label1, alpha=alpha[num])

        plt.setp(axis.get_xticklabels(), visible=True)
        plt.setp(axis.get_yticklabels(), visible=True, fontsize=ytic_size)
        # Show grid
        plt.grid()
        plt.axhline(y=1, ls='--', c='k', lw=0.8)

        # Show legend
        # plt.legend(prop={'size':8})
        axis.yaxis.set_label_text(
            r'$ \beta $', fontsize=ylab_font, fontweight='bold')  # ("$|B| [nT]$")
        plt.yscale('log')
        draw_vertical(euhforia_earth_beta_spr, final_dates1, axis)

        num = num+1

    #----------- Overall plot formatting -----------#
    font = FontProperties()
    font.set_family('serif')
    font.set_name('Times New Roman')
    # x axis format
    myFmt = mdates.DateFormatter('%Y-%m-%d %H:%M')  # %d-%m-%y')#
    axis.xaxis.set_major_formatter(myFmt)
    # rotating labels
    fig.autofmt_xdate()

    #ax.xaxis.set_major_locator( MultipleLocator(20) )
    axis.xaxis.set_minor_locator(
        AutoMinorLocator(6))  # ( MultipleLocator(10) )

    axis.set_xlim((start_date, end_date))
    plt.setp(axis.get_xticklabels(), visible=True, fontsize=xtic_size)
    axis.xaxis.set_label_text("$Date$", fontsize=xlab_font, fontweight='bold')
    fig.align_ylabels()
    # plt.tight_layout()

    # fig.suptitle(suptitle)
    fig.tight_layout()

    plt.savefig(output_dir + png_name, dpi=400, bbox_inches="tight")
    plt.close(fig)
