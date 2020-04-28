import math
import numpy as np
from scipy.interpolate import interp1d
from aerodynamics import aero
from propulsion import prop
from atmosphere import atmo_ISA
from constants import const
from user import aeromodel, vehicle

def dynamics(t, x0, control):
    #vehicle compenents
    vehicle_Sgross = vehicle()

    #constants
    const_J2 = const()[4]
    const_wE = const()[2]
    const_J3 = const()[5]
    const_mu = const()[3]
    const_J4 = const()[6]
    const_flatE = const()[1]
    const_aE = const()[0]

    #state vector compenents
    h = max(x0[0],0) #altitude from surface to vehicle, m
    v = x0[1] #vehicle velocity relative to earth, m/s
    fpa = x0[2] #flight path angle, radians
    chi = x0[3] #flight heading angle, radians
    lat = x0[4] #latitude (+North), radians
    lon = x0[5] #longitude (+East), radians
    m = x0[6]    #vehicle mass, kg
    #mach = x0[7] #inital mach no
    #Earth and gravity model
    rE = const_aE*(1-const_flatE*math.sin(lat)**2) #values for spheroid
    r = h + rE

    atmo=atmo_ISA(h)
    press = atmo[0]
 #   temp = atmo[1]
    dens = atmo[2]
    sspeed = atmo[3]

    #4th degree, zonal harmonic Earth gravity model
    phi = math.pi/2-lat
    gr = (const_mu/r**2*(1 - 1.5*const_J2*(3*math.cos(phi)**(2)-1)*(rE/r)**(2)-2*const_J3* \
    math.cos(phi)*(5*math.cos(phi)**(2)-3)*(rE/r)**(3)-(5/8)*const_J4*(35*math.cos(phi)**(4)-30*math.cos(phi)**(2)+3)* \
    (rE/r)**(4)))
    gt =-3*const_mu*math.sin(phi)*math.cos(phi)*(rE/r)**(2)*(const_J2+0.5*const_J3*(5*math.cos(phi)**(2)-1)* \
    (rE/r)/math.cos(phi)+(5/6)*const_J4*(7*math.cos(phi)**(2)-1)*(rE/r)**(2))/r**(2)

    #control law (h-alpha)
    fa = interp1d(control[0,:], control[1,:], kind='cubic')
    alpha = fa(t)
    bank=0
    ft = interp1d(control[0,:], control[2,:], kind='cubic')
    throttle = ft(t)

    #Aerodynamics components
    if aeromodel() == 1:
        CD = aero()[0]
        CL = aero()[1]
    elif aeromodel() == 2:
        CD = aero()[2]
        CL = aero()[3]
    elif aeromodel() == 3:
        CD = aero()[4]
        CL = aero()[5]

    #Propulsion components
    pc = prop(throttle, press)
    FT = pc[0]
    mp = pc[1]

    #Atmospheric Model
    #dmach = math.fabs(v)/sspeed

    #Aerodynamics model
    qdyn = 0.5*dens*v**2
    L = CL*vehicle_Sgross*qdyn
    D = CD*vehicle_Sgross*qdyn

    #Equations of motion
    dh = v*math.sin(fpa)
    dlat = (v*math.cos(fpa)*math.cos(chi)/r)

    if math.fabs(lat-math.pi/2) < np.spacing(1):
        dlon = 0
    else:
        dlon = v*math.cos(fpa)*math.sin(chi)/(r*math.cos(lat))

    Fx = (FT*math.cos(alpha)-D)/m-gr*math.sin(fpa)+gt*math.cos(fpa)*math.cos(chi)
    dv = Fx+const_wE**(2)*r*math.cos(lat)*(math.sin(fpa)*math.cos(lat)-math.cos(fpa)*math.cos(chi)*math.sin(lat))

    if math.fabs(v) < np.spacing(1):
        dfpa = 0
    else:
        Fz = (FT*math.sin(alpha)+L)*math.cos(bank)/m-gr*math.cos(fpa)-gt*math.sin(fpa)*math.cos(chi)
        dfpa = (v/r)*math.cos(fpa)+Fz/v+(const_wE**(2)*r/v)*math.cos(lat)*(math.sin(fpa)*math.cos(chi)*math.sin(lat)+math.cos(fpa)*math.cos(lat))+2*const_wE*math.sin(chi)*math.cos(lat)

    if math.fabs(lat - math.pi/2) < np.spacing(1) or math.fabs(lat + math.pi/2) < np.spacing(1) or math.fabs(fpa - math.pi/2) < np.spacing(1) or math.fabs(v) < np.spacing(1):
        dchi = 0
    else:
        Fy = (FT*math.sin(alpha)+L)*math.sin(bank)/m - gt*math.sin(chi)
        dchi = (v/r)*math.cos(fpa)*math.sin(chi)*math.tan(lat) + Fy/(v*math.cos(fpa)) \
        + const_wE**(2)*r*(math.sin(chi)*math.sin(lat)*math.cos(lat))/(v*math.cos(fpa)) + 2*const_wE*(math.sin(lat)-math.tan(fpa)*math.cos(chi)*math.cos(lat))
    dm = -mp

    return [dh, dv, dfpa, dchi, dlat, dlon, dm]
