import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import newton
from scipy.optimize import bisect
import mod
import dgl
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

params = {
    'P': 2e10,
    'T0_so': 293,
    'T0_sub': 293,
    't_range': [0,1000],
    'pulsed': True,
    'f': 0.1,
    't_p': 1e0,
    'n': 100,
    'thick0': 0.0,
    }

def calc_res(P, t_end=100, t_p=None, n=10, pulsed=False):
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
    return result

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
    thickness_pulse = calc_res(P_pulse, t_end, t_p, n, pulsed=True)['Thickness'][-1]
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
    # try to find the point where the function crosses the x-axis. If ValueError is raised, return NaN
    try:
        bisection = bisect(func, 0, b, args=args, xtol=1)
        opt_power = newton(func, bisection, args=args, tol=0.01)
    except ValueError:
        opt_power = np.NaN
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
        for r in tqdm(rate_vals):
            p_opt.append(find_power(difference, 1e5, args=(tp0, r, 100, 10)))
    p_opt = np.array(p_opt).reshape(len(t_p), len(rate_vals))
    print('Calculation of optimal powervalues is done.')
    return p_opt

def calc_single_power(args):
    tp0, r = args
    return find_power(difference, 1e5, args=(tp0, r, 100, 10))

def calc_p_opt_parallel(t_p, rate_vals):
    print('Calculation of optimal power values is running...')
    tp_r_combinations = [(tp0, r) for tp0 in t_p for r in rate_vals]

    with ProcessPoolExecutor() as executor:
        p_opt = list(executor.map(calc_single_power, tp_r_combinations))

    p_opt = np.array(p_opt).reshape(len(t_p), len(rate_vals))
    print('Calculation of optimal power values is done.')
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
    temps = []
    thicks = []    
    print('Calculation of temperatures is running:')
    for i in range(len(t_p)):
        for p in range(len(rate_vals)):
            if np.isnan(p_opt[i][p]):
                print(f'No optimal power found for t_p={t_p[i]:.1f} s and rate={rate_vals[p]:.1f} A/s')
                temps.append(np.NaN)
                thicks.append(np.NaN)
            else:
                res = calc_res(P=p_opt[i][p], t_p=t_p[i], pulsed=True)
                thickness, temperature = res['Thickness'][-1], max(res['Temp_substrate'])
                print(f'Thickness: {thickness:.2f} A, Temperature: {temperature:.2f} K')
                temps.append(temperature)
                thicks.append(thickness)
    print('Calculation of temperatures is done.')
    return temps, thicks


def calc_temp_single(args):
    t_p, rate, p_opt = args
    if np.isnan(p_opt):
        return np.NaN, np.NaN
    else:
        res = calc_res(P=p_opt, t_p=t_p, pulsed=True)
        thickness, temperature = res['Thickness'][-1], max(res['Temp_substrate'])
        return thickness, temperature

def calc_temp_parallel(t_p, rate_vals, p_opt):
    print('Calculation of temperatures is running...')
    args_list = [(t_p[i], rate_vals[j], p_opt[i][j]) for i in range(len(t_p)) for j in range(len(rate_vals))]

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(calc_temp_single, args_list))

    thicks, temps = zip(*results)
    temps = np.array(temps).reshape(len(t_p), len(rate_vals))
    thicks = np.array(thicks).reshape(len(t_p), len(rate_vals))
    print('Calculation of temperatures is done.')
    return temps, thicks