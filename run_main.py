# -*- coding: utf-8 -*-
"""
Main run file for Calum Park
Research project on integrating odes for
TROPICO in Python
"""
from scipy.integrate import solve_ivp
import math
import numpy as np
from dynamics_me import dynamics
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#state vector components
h = 45000.0 #altitude from surface to vehicle, m
v =  1341.1 #vehicle velocity relative to earth, m/s
fpa = math.pi/2 #flight path angle, radians
chi = math.pi/2  #flight heading angle, radians
lat =  0.4987  #latitude (+North), radians
lon = -1.4076 #longitude (+East), radians
m = 860326.0    #vehicle mass, kg
x0 = [h, v, fpa, chi, lat, lon, m]

tof=[0, 360]

#more AoA can be added, array must have at least 3 values even if constant
#no of throttle values must = no of AoA values, even if throttle is constant
alpha = np.array([0.0, 0.0, 0.0, 0.01745, 0.0523599, 0.0872665, 0.0, 0.0, 0.0]) #angle of attack, radians -0.1745, -0.2443, -0.1047, 0.01745, 0.0698, -0.01745, 0.0, 0.0, 0.0
throttle =  np.array([1.0, 9.0, 8.0, 7.0, 7.0, 6.0, 6.0, 5.0, 5.0]) #between 0-1
utime = np.linspace(tof[0], tof[1], len(alpha))
control = np.array([utime, alpha, throttle])

#d = dynamics(4,x0,control)
#print d

#scipy.integrate.solve_ivp(fun, t_span, y0, method='RK45', t_eval=None, dense_output=False, events=None, vectorized=False, args=None, **options)
sol = solve_ivp(lambda t, x: dynamics(t, x, control), tof, x0, dense_output=True, max_step=0.9, atol = 1, rtol = 1)

print sol.t

#if  lat/lon doesn't change by 1 dgree, assumed straight vertical/horizantal flight
# if math.fabs(sol.y[4,-1] - sol.y[4,0]) < 0.00174533:
#     sol.y[4,:] = sol.y[4,0]
# if math.fabs(sol.y[5,-1] - sol.y[5,0]) < 0.00174533:
#     sol.y[5,:] = sol.y[5,0]

print sol.y

#plotting of trajectory
fig1 = plt.figure()
ax1 = fig1.add_subplot(111, projection='3d')
ax1.plot(sol.y[5,:], sol.y[4,:], sol.y[0,:])    #x-axis: longitude (radians), y-axis: latitude (radians), z-axis: altitude (meters)
ax1.set_title('Trajectory of Vehicle')
ax1.set_xlabel('Longitude (Radians)')
ax1.set_ylabel('Latitude (Radians)')
ax1.set_zlabel('Altitude (m)')

#plotting of flight data
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.plot(sol.t, sol.y[0,:])
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Altitude (m)')
ax2.set_title('Flight Data - Altitude vs Time')

fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
ax3.plot(sol.t, sol.y[2,:])
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Velocity (m/s)')
ax3.set_title('Flight Data - Velocity vs Time')

fig4 = plt.figure()
ax4 = fig4.add_subplot(111)
ax4.plot(sol.t, sol.y[6,:])
ax4.set_xlabel('Time (s)')
ax4.set_ylabel('Mass (kg)')
ax4.set_title('Flight Data - Mass vs Time')

#fig6 = plt.figure()
# ax6 = fig6.add_subplot(111)
# ax6.plot(np.linspace(tof[0],tof[1],len(control[1])), control[1,:]*180/math.pi, marker = '.')
# ax6.set_xlabel('Time (s)')
# ax6.set_ylabel('Angle of Attack (Degree)')
# ax6.set_title('Flight Data - Angle of Attack vs Time')

#fig5 = plt.figure()
# ax5 = fig5.add_subplot(111)
# ax5.plot(np.linspace(tof[0],tof[1],len(control[2])), control[2,:], marker = '.')
# ax5.set_xlabel('Time (s)')
# ax5.set_ylabel('Throttle')
# ax5.set_title('Flight Data - Throttle vs Time')

plt.show()
