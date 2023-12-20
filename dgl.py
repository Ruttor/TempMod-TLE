# Faktoren vor den Termen in den DGL's
c = {
    'source_therm_cap': 0.0133, # thermal capacity source
    'source_radiation': 4e-10, # radiative heat emission at source
    'laser_power': 0.5, # laser power
    'sub_therm_cap': 6.722, # thermal capacity source
    'sub_absorption': 1.88e-11, # radiative heat absorption at substrate from source
    'sub_radiation': 1.149e-10, # radiative heat emission at substrate
    'gr_factor': 8e1, # growth rate factor '' e^(-1/T)
    'gr_exp': 1.128e3, # growth rate exponent factor e^(- '' /T)
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
    T_punkt_so = c['source_therm_cap'] * (- c['source_radiation'] * T_so**4 + c['laser_power'] * P)  # calculate derivative of surface temperature
    T_punkt_sub = c['sub_therm_cap'] * (c['sub_absorption'] * T_so**4 - c['sub_radiation'] * T_sub**4)  # calculate derivative of substrate temperature
    T_punkt = (T_punkt_so, T_punkt_sub,)  # pack derivative of surface and substrate temperature

    return T_punkt