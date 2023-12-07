import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from tqdm import tqdm

class TempMod:
    """Class for calculating the temperature at the surface and at the substrate.

    Attributes
    ----------
    func (function):
        Function to calculate the temperature at the surface and at the substrate.
    """

    def __init__(self, func):
        self.func = func

    def mod(self,P,T0_so,T0_sub,t_range=False,pulsed=False,f=None,t_p=None,n=None,thick0=0, gr_factor=1e0, gr_exp=1e3):
        """Calculate the temperature at the surface and substrate.

        Parameters
        ----------
        P (float):
            Laser power
        T0_so (float):
            Surface temperature
        T0_sub (float):
            Substrate temperature
        t_range (list):
            Time range [start, end] (default: False)
        pulsed (bool):
            Whether it's pulsed laser heating (default: False)
        f (float):
            Frequency (required if pulsed is True)
        t_p (float):
            Pulse duration (required if pulsed is True)
        n (int):
            Number of pulses (required if pulsed is True)
        thick0 (float):
            Initial thickness of the grown layer (default: 0)

        Returns
        -------
        dict: A dictionary containing Time, Temp_source, Temp_substrate, Power, Thickness, and Growth_rate.
        """

        T_source, T_substrate, power, time = self.__calc_temps(P, T0_so, T0_sub, t_range, pulsed, f, t_p, n)  # Calculate the temperature at the surface and substrate, as well as power and time
        thick, growth_rate = self.__calc_thick(T_source, time, thick0, gr_factor, gr_exp)  # Calculate the thickness of the grownlayer

        return {
            "Time": time,
            "Temp_source": T_source,
            "Temp_substrate": T_substrate,
            "Power": power,
            "Thickness": thick,
            "Growth_rate": growth_rate,
        }

    def __calc_temps(self, P, T0_so, T0_sub, t_range=False, pulsed=False, f=None, t_p=None, n=None):
        """Calculate the temperature at the surface and at the substrate.

        Returns
        -------
        T_source (list):
            Temperature at the surface
        T_substrate (list):
            Temperature at the substrate
        power (list):
            Laser power
        time (list):
            Time
        """

        # Create lists to store the temperature at the surface and substrate, as well as power and time
        T_source = []
        T_substrate = []
        power = []
        time = []

        T0 = (T0_so, T0_sub)  # Starting conditions
        if pulsed:  # If it's pulsed laser heating with a sqaure pulse
            if not f or not t_p or not n:  # Check if f, t_p, and n are provided
                raise ValueError("f, t_p, and n are required for pulsed laser heating.")

            for i in range(2 * n): # Iterate over frequency sections
                if i % 2 == 0:  # Active Laser
                    P_in = P  # Set the power to P
                    t = np.linspace(i / (2 * f), i / (2 * f) + t_p, 1000)  # Time range of the active pulse
                    # 1/(2f) = index has to be devided by 2 because the iteration range is 2*n
                    # i / (2f) = startingpoint of the pulse
                    # i / (2f) + t_p = endpoint of the pulse
                else:  # No laser
                    P_in = 0  # Set the power to 0
                    t = np.linspace((i - 1) / (2 * f) + t_p, (i + 1) / (2 * f), 1000)  # Time range between the pulses
                    # 1/(2f) = index has to be devided by 2 because the iteration range is 2*n
                    # (i - 1) / (2f) + t_p = set start at end of pulse calculated at previous index, therefore (i-1)
                    # (i + 1) / (2f) = set end at start of pulse calculated at next index, therefore (i+1)
                    
                T = odeint(self.func, T0, t, args=(P_in,))  # Calculate the temperatures
                T0 = T[-1]  # Set the starting conditions to the last element of the temperatures

                # Append the temperatures, power, and time to the lists
                T_source.extend(T[:, 0])
                T_substrate.extend(T[:, 1])
                time.extend(t)
                power.extend([P_in] * len(t))

        else:  # If it's continuous laser heating
            if not t_range:  # Check if t_range is provided
                raise ValueError("t_range is required for continuous laser heating.")

            t = np.linspace(t_range[0], t_range[1], int(100 * t_range[1]))  # Time range of active laser
            T = odeint(self.func, T0, t, args=(P,))  # Calculate the temperatures

            # Append the temperatures, power, and time to the lists
            T_source.extend(T[:, 0])
            T_substrate.extend(T[:, 1])
            time.extend(t)
            power.extend([P] * len(t))

        return np.array(T_source), np.array(T_substrate), np.array(power), np.array(time)

    def __calc_thick(self, T_source, time, thick0, gr_factor, gr_exp):
        """Calculate the thickness of the grown layer.

        Returns
        -------
        thick (list):
            Thickness of the grown layer
        growth_rate (list):
            Growth rate of the grown layer
        """
        time = [time[0]] + time  # Create a list of time with an additional element being the initial time to keep the same length as T_source in the following calculations
        delta_t = np.diff(time)  # Calculate the time interval
        growth_rate = gr_factor * np.exp(- gr_exp / T_source)  # Calculate the growth rate
        thick = np.zeros(len(T_source))  # Create initial thickness
        thick[0] = thick0  # Set the initial thickness

        for i in range(len(T_source) - 1):  # Calculate the thickness at each time step
            thick[i + 1] = (thick[i] + growth_rate[i] * delta_t[i])  # Calculate the thickness at each time step using the previous thickness and growth rate

        return thick, growth_rate
