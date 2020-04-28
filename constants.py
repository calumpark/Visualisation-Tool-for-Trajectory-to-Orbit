import numpy as np
from math import sqrt

#Ideally would use const.__ using classes but struggling to workout how to do this

def const():
#Constants for Earth ellipsoidal model
#Enhanced WGS-84(1984)
    const_aE = 6378137.0 # Semi-major axis (m) of Earth
    const_flatE = 1/298.257223563  #Earth flattening
    const_wE = 7.292115e-5  # Angular rotation of the Earth (rad/s)

# Gravitational constants
    const_mu = 3.986004418e14 # Geocentric constant of gravitation (GM) [m3/s2]
    const_J2 = 1.08264e-3 # Second degree term in Earth's gravity potential
    const_J3 = -2.546e-6
    const_J4 = -1.649e-6

    const = np.array([const_aE, const_flatE, const_wE, const_mu, const_J2, const_J3, const_J4])
    return const
