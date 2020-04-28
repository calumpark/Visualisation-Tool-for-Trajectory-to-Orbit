import numpy as np

def prop(throttle, press):
    Aexit = 2.3 #2.9 #nozzle exit diameter, m

    T1 = 5.255e6 * throttle
    Isp = 452   #specific impulse
    mix_ratio = 6.0

    mp_fuel = (4 * T1 / (Isp*9.80665))/(1+mix_ratio)
    mp_ox = mp_fuel * mix_ratio

    T = 4 * (T1 - Aexit * press)
    FT = max(min(T, 1e8),0)
    mp = mp_fuel + mp_ox
    return [FT, mp]
