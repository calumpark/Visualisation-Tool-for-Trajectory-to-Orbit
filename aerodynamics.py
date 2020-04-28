import numpy as np
#from user import aerodynamics

#could let user input own CL and CD and have option of choosing one of set ones

def aero():

    CD1 = 0.0     #aero none
    CL1 = 0.0

    CD2 = 0.75  #aero rocket
    CL2 = 0.0

    CD3 = 0.0244     #aero spaceplane
    CL3 = 0.508

    aero = np.array([CD1, CL1, CD2, CL2, CD3, CL3])
    return aero
