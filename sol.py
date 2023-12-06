import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import newton
from scipy.optimize import bisect
import mod
import dgl
from tqdm import tqdm

params = {
    'P': 2e5,
    'T0_so': 1e-14,
    'T0_sub': 0e0,
    't_range': [0,100],
    'pulsed': True,
    'f': 0.1,
    't_p': 1e0,
    'n': 10,
    'thick0': 0.0,
    }

def thickness(P, t_end=100, t_p=None, n=10, pulsed=False):
    """Calculates the thickness of the grown layer and the maximum substrate temperature.
    
    Parameters
    ----------
    P : float
        Laser power
    t_end : float
        End time (default: 100)
    t_p : float
        Pulse duration (required if pulsed is True)
    n : int
        Number of pulses (required if pulsed is True)
    pulsed : bool
        Whether it's pulsed laser heating (default: False)
    
    Returns
    -------
    tuple: A tuple containing the thickness of the grown layer and the maximum substrate temperature.
    """
    # raises Valuerror if t_p is not given, but pulsed is True
    if pulsed and not t_p:
        raise ValueError("t_p is required for pulsed laser heating.")
    
    tm = mod.TempMod(dgl.T_punkt) # Initializes the TempMod class
    if pulsed:
        result = tm.mod(P=P, T0_so=params['T0_so'], T0_sub=params['T0_sub'], pulsed=pulsed, f=params['f'], t_p=t_p, n=n, gr_factor=dgl.c['gr_factor'], gr_exp=dgl.c['gr_exp'])
    else:
        result = tm.mod(P=P, T0_so=params['T0_so'], T0_sub=params['T0_sub'], t_range=[0, t_end], gr_factor=dgl.c['gr_factor'], gr_exp=dgl.c['gr_exp'])
    # Returns the last thickness and the maximum substrate temperature
    return result['Thickness'][-1], result['Temp_substrate'].max()

def difference(P_pulse, t_p, rate, t_end, n):
    """Calculates the difference between the thickness of the grown layer for constant and pulsed laser heating.
    
    Parameters
    ----------
    P_pulse : float
        Laser power
    t_p : float
        Pulse duration
    rate : float
        Rate of the laser heating
    t_end : float
        End time
    n : int
        Number of pulses
    cache : dict
        Cache for the results (default: {})
    
    Returns
    -------
    float: The difference between the thickness of the grown layer for constant and pulsed laser heating.
    """
    # Calculates the thickness of the grown layer for constant laser heating
    thickness_const = rate * t_end
    thickness_pulse, _ = thickness(P_pulse, t_end, t_p, n, pulsed=True)
    diff = thickness_const - thickness_pulse
    return diff


def find_power(func, b, args=()):
    """Calculates the points of a function where it crosses the x-axis (optimal power).
    
    Parameters
    ----------
    func : function
        Function which varies the power in order to reduce the difference of thickness between constant and pulsed laser heating
    b : float
        Upper bound for the power
    args : tuple
        Arguments for the function (default: ())
    
    Returns
    -------
    float: The optimal power
    """
    bisection = bisect(func, 0, b, args=args, xtol=1)
    opt_power = newton(func, bisection, args=args, tol=0.01)
    return opt_power

def calc_p_opt(t_p, rate_vals):
    """Calculates the optimal power for different pulse durations and rates.
    
    Parameters
    ----------
    t_p : list
        List of pulse durations
    rate_vals : list
        List of rates
    
    Returns
    -------
    array: Array containing the optimal power for different pulse durations and rates
    """
    p_opt = []
    print('Calculation of optimal powervalues is running:')
    for tp0 in t_p:
        print(f'Calculation for t_p={tp0:.1f} s:')
        for r in rate_vals:
            p_opt.append(find_power(difference, 1e3, args=(tp0, r, 100, 10)))
    p_opt = np.array(p_opt).reshape(len(t_p), len(rate_vals))
    print('Calculation of optimal powervalues is done.')
    return p_opt
    
def calc_temp(t_p, rate_vals, p_opt):
    """Calculates the temperatures for different pulse durations and rates.
    
    Parameters
    ----------
    t_p : list
        List of pulse durations
    rate_vals : list
        List of rates
    p_opt : array
        Array containing the optimal power for different pulse durations and rates
    
    Returns
    -------
    tuple: Tuple containing the temperatures and the thicknesses for different pulse durations and rates
    """
    colormap_data = []
    colormap_data_thick = []    
    print('Calculation of temperatures is running:')
    for i in range(len(t_p)):
        for p in range(len(rate_vals)):
            thickness_solved, temperature = thickness(P=p_opt[i][p], t_p=t_p[i], pulsed=True)
            print(f'Thickness: {thickness_solved:.2f} A, Temperature: {temperature:.2f} K')
            colormap_data.append(temperature)
            colormap_data_thick.append(thickness_solved)
    print('Calculation of temperatures is done.')
    return colormap_data, colormap_data_thick

def create_colormap(rate, pulse_durations, temp):
    # Creates a meshgrid for the colormap
    p, T_p = np.meshgrid(rate, pulse_durations)
    # Converts the temperatures into an array and reshapes it into the right shape (2D)
    Temps = np.array(temp).reshape(len(rate), len(pulse_durations))
    # Creates the colormap
    plt.figure(figsize=(8, 6))
    plt.imshow(Temps, extent=(p.min(), p.max(), T_p.min(), T_p.max()), origin='lower', aspect='auto', cmap='inferno')
    # currently german labels because I need them for my thesis (will be changed in the future)
    plt.colorbar(label='Substrattemperatur')
    plt.xlabel('Rate')
    plt.ylabel('Pulsdauer')
    plt.title('Temperatur Colormap')
    plt.show()