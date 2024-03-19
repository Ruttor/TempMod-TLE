# Faktoren vor den Termen in den DGL's
import numpy as np
# c = {
#     'source_therm_cap': 0.133, # thermal capacity source
#     'source_radiation': 4e-13, # radiative heat emission at source
#     'laser_power': 1, # laser power
#     'sub_therm_cap': 3.7, # thermal capacity source
#     'sub_absorption': 1.88e-14*1e4, # radiative heat absorption at substrate from source
#     'sub_radiation': 4.6e-10, # radiative heat emission at substrate
#     'gr_factor': 1.3e18, # growth rate factor '' e^(-1/T)
#     'gr_exp': 5e5 *1e-2, # growth rate exponent factor e^(- '' /T)
#     'ambient_temperature': 293, # ambient temperature
#     'vwl': 1.3e18 *1e-2, # verdampfungswärmeleistung  # Sollwert ist 1.13e18 1.13e17 ist zu groß und 1.13e16 hat keinen Einfluss
#     'wl': 1e-3 *1e3, # wärmeleitung
#     }
c = {
    'source_therm_cap': 0.133, # thermal capacity source
    'source_radiation': 4e-13, # radiative heat emission at source
    'laser_power': 1, # laser power
    'sub_therm_cap': 3.7, # thermal capacity source
    'sub_absorption': 1.88e-13*1e3, # radiative heat absorption at substrate from source
    'sub_radiation': 4.6e-10, # radiative heat emission at substrate
    'gr_factor': 1.3e18, # growth rate factor '' e^(-1/T) 
    'gr_exp': 51118, # growth rate exponent factor e^(- '' /T)
    'ambient_temperature': 293, # ambient temperature
    'vwl': 1.3e18, # verdampfungswärmeleistung
    'wl': 1e-3*1e1, # wärmeleitung
    }

# Zu lösendes Differentialgleichungssystem
def T_punkt(T, t, P):
    """Calculate the derivative of the temperature at the surface and at the substrate.

    Parameters
    ----------
    T : tuple
        Initial surface and substrate temperature
    t : float
        Time

    Returns
    -------
    T_punkt : tuple
        Derivative of the surface and substrate temperature
    """
    T_so, T_sub = T  # unpack initial temperatures
    T_punkt_so = 1/c['source_therm_cap'] * (- c['source_radiation'] * (T_so**4-c['ambient_temperature']**4) - c['vwl']*np.e**(-c['gr_exp']/T_so) - c['wl']*(T_so-c['ambient_temperature']) + c['laser_power'] * P)  
    T_punkt_sub = 1/c['sub_therm_cap'] * (c['sub_absorption'] * T_so**4 - c['sub_radiation'] * (T_sub**4-c['ambient_temperature']**4))  # calculate derivative of substrate temperature
    T_punkt = (T_punkt_so, T_punkt_sub,)  # pack derivative of surface and substrate temperature

    return T_punkt