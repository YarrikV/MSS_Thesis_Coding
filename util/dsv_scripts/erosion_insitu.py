
#!/usr/bin/env python

"""
Calculates erosion
"""
from util import *


loc = 'Earth'  # 'SC016'

date_beg = "2012-07-11T00:00:00"
date_end = "2012-07-19T00:00:00"

# time interval you want to plot
start_date = datetime.strptime(
    date_beg, "%Y-%m-%dT%H:%M:%S")  # 2020-05-14T02:00:00
end_date = datetime.strptime(
    date_end, "%Y-%m-%dT%H:%M:%S")  # 2020-05-17T00:00:00

dd = '20120712'
yr = '2012'

# directory where data are stored
data_dir = './mass111-test/'
t7 = './mass111-test/'

# PLOTTING CONSTANTS
color = ['b-', 'r-', 'm-', 'g-', 'k-', 'c-', 'b--', 'r--', 'm--']
alpha = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5]
lw = [2, 2, 2, 2, 1.2, 1.2, 1.2, 1.2, 1.2]
ytic_size = 12
xtic_size = 10
ylab_font = 12
xlab_font = 12

dsv = [t7]
lbl = ['testlabel']
infile = ['m_sph_'+loc]

png_name = 'test'

suptitle = 'Earth'

# directory where plots will be stored
output_dir = './output/'

# constants
mu_0 = 4*np.pi*(10**(-7.))  # vacuum magnetic permeability [SI: N / A^2]
mu = 1              # mean molecular weight of the plasma
m_p = 1.6726 * (10**(-27.))     # proton mass [kg]
kB = scipy.constants.k

lw = 1.0

num = 0

# for all dsv files
for i in dsv:

    date = '20120712'

    # directory where data are stored
    data_dir_spr = i

    # --------------------------------------------------------
    # READING IN EUHFORIA DATA
    # --------------------------------------------------------

    file_spr = []
    # input files from EUHFORIA
    file_spr.append(i + infile[num] + ".dsv")

    print("Files loaded:")

    print(file_spr)

    # column format in euhforia data file
    data_earth_spr = np.loadtxt(file_spr[0], delimiter=' ', skiprows=1, usecols=[
                                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    print(len(data_earth_spr))

    # dates
    date_earth1 = np.loadtxt(
        file_spr[0], delimiter=' ', dtype='str', skiprows=1, usecols=[0])

    # assigning date to euhforia data
    final_dates1 = []
    for dates in date_earth1:
        final_dates1.append(datetime.strptime(
            str(dates), "%Y-%m-%dT%H:%M:%S"))

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
    # [in the order of 10^{-12} Pa]
    euhforia_earth_p_therm_spr = data_earth_spr[:, 4]
    euhforia_earth_p_mag_spr = (
        (euhforia_earth_b_spr*10**-9.0)**2.0)/(2.0*(10**-7))
    euhforia_earth_p_int_spr = euhforia_earth_p_therm_spr + euhforia_earth_p_mag_spr

    # negative pressure in the domain.... Alert alert alert.
    euhforia_earth_beta_spr = euhforia_earth_p_therm_spr/euhforia_earth_p_mag_spr

    # defining number density
    euhforia_earth_n_spr = 0.5*data_earth_spr[:, 3]
    euhforia_earth_p_dyn_spr = euhforia_earth_n_spr*1e6 * \
        m_p*euhforia_earth_v_spr*euhforia_earth_v_spr*1e6

    # --------------------------------------------------------------------------------------------------------
    # PLOTTING ----------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------

    fig, axs = plt.subplots(5)
    fig.suptitle('Extracting magnetic cloud '+'\n'+lbl[num])

    # --------------------------------------------------------------------------------------------------------
    # -Vx
    # --------------------------------------------------------------------------------------------------------

    ax = axs[0]
    ax.plot(final_dates1, -euhforia_earth_vx_spr, label='- Vx')
    draw_vertical(euhforia_earth_beta_spr, final_dates1, ax)
    plt.setp(ax.get_xticklabels(), visible=False)

    # --------------------------------------------------------------------------------------------------------
    # Plasma beta
    # --------------------------------------------------------------------------------------------------------

    ax = axs[1]
    ax.plot(final_dates1, euhforia_earth_beta_spr, label='$\beta$')
    ax.set_yscale('log')
    ax.axhline(y=1, c='k', linestyle='--', linewidth=lw)
    ax.axhline(y=0.1, c='k', linestyle='--', linewidth=lw)
    plt.setp(ax.get_xticklabels(), visible=False)

    # MC start and end times
    tfront, trear, ind_front, ind_rear = draw_vertical(
        euhforia_earth_beta_spr, final_dates1, ax)
    print(tfront, trear)
    print(ind_front, ind_rear)

    # --------------------------------------------------------------------------------------------------------
    # Thermal and magnetic pressure
    # --------------------------------------------------------------------------------------------------------

    ax = axs[2]
    ax1 = ax.twinx()
    ax.plot(final_dates1, euhforia_earth_p_therm_spr, label='$P_{therm}$')
    plt.legend()

    ax1.plot(final_dates1, euhforia_earth_p_mag_spr,
             color='r', label='$P_{mag}$')
    tfront, trear, ind_front, ind_rear = draw_vertical(
        euhforia_earth_beta_spr, final_dates1, ax)
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.legend()

    '''
    #Below, the azimuthal flux has been summed up in the MC along the passage of the spacecraft.
    erosion = l_fr*np.sum(phi_y_by_l(ind_front,ind_rear,euhforia_earth_by_spr,euhforia_earth_vx_spr)) #[Wb]
    print ("Erosion [Wb]: ","{:e}".format(erosion))
    print ("Length FR [m]: ", "{:e}".format(l_fr))
    '''

    # --------------------------------------------------------------------------------------------------------
    # By and phiy_over_l
    # --------------------------------------------------------------------------------------------------------

    ax = axs[3]
    ax.plot(final_dates1, euhforia_earth_by_spr, '-b', label='By')
    ax.yaxis.set_label_position("left")
    ax.yaxis.tick_left()
    ax.axhline(y=0, c='k', linestyle='--', linewidth=lw)
    ax.set_ylim((-70, 57))
    ax2 = ax.twinx()
    rad_spr = 16*R_sun/au  # [m]
    l_fr = 2.0*np.pi*rad_spr
    erosion = phi_y_by_l(ind_front, ind_rear, euhforia_earth_by_spr,
                         euhforia_earth_vx_spr, final_dates1)  # [Mx]
    ax2.plot(final_dates1[ind_front:ind_rear],
             erosion, '-r', label='phi_y over l [Wb]')
    #ax2.axhline(y=np.sum(erosion), c='m',linestyle='--', linewidth=lw, label='phi_erosion')

    ind_center = find_mc_centre(euhforia_earth_by_spr, final_dates1, ax2)

    phi_az = ((phi_y_by_l(ind_center, ind_rear, euhforia_earth_by_spr,
                          euhforia_earth_vx_spr, final_dates1)))
    ax2.plot(final_dates1[ind_center:ind_rear],
             phi_az, '-g', label='phi_az [Wb]')
    #ax2.axhline(y=phi_az, c='k',linestyle='--', linewidth=lw, label='phi_az')
    ax2.axhline(y=0, c='k', linestyle='-', linewidth=lw)

    print('Flux eroded (total phiy_over_l) = ', np.sum(erosion))
    print(
        'Flux eroded (absolute phiy_over_l[-1]/phi_az) = ', erosion[-1]/(2*np.sum(phi_az)))
    print(
        'Flux eroded (absolute phiy_over_l[0]/phi_az) = ', erosion[0]/(2*np.sum(phi_az)))

    # Multiplied with two assuming the flux in the trailing part is the same as the leading part of the MC
    print('Flux azimuthal (non-eroded) = ', 2*np.sum(phi_az))

    # To find where phiy_over_l crosses zero
    for i in range(ind_front, ind_rear-1):
        if np.sign(erosion[i-ind_front]) != np.sign(erosion[i-ind_front-1]):
            ax2.axvline(x=final_dates1[i], c='y',
                        linestyle='--', linewidth=lw)

    ax2.yaxis.set_label_position("right")
    ax2.yaxis.tick_right()
    draw_vertical(euhforia_earth_beta_spr, final_dates1, ax)
    plt.setp(ax.get_xticklabels(), visible=False)

    # --------------------------------------------------------------------------------------------------------
    # Bz
    # --------------------------------------------------------------------------------------------------------

    ax = axs[4]
    ax.plot(final_dates1, euhforia_earth_bz_spr, '-b', label='Bz')
    ax.axvline(x=final_dates1[ind_center], c='k',
               linestyle='--', linewidth=lw)
    ax.axhline(y=0, c='k', linestyle='--', linewidth=lw)
    draw_vertical(euhforia_earth_beta_spr, final_dates1, ax)
    plt.legend()

    plt.show()

    num += 1
