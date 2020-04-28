
def vehicle():
    vehicle_Sgross = 10.0 #gross wing area, m^2
    return vehicle_Sgross

def aeromodel():
    aero_model = 3   #select an aerodynamic model
#                      enter 1 for none (CL = 0, CD = 0)
#                      enter 2 for rocket (CL = 0, CD = 0.75)
#                      enter 3 for spaceplace (CL = 4.05, CD = 0.0618)
    return aero_model

# def propmodel():
#     prop_model = 1   #select an propulsion model
# #                      enter 1 for simple (FT = 0, mp = 0)
# #                      enter 2 for rocket (depends on throttle and pressure)
#     return prop_model
