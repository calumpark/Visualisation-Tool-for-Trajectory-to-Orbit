#atmospheric model
import math

def atmo_ISA(alt):

    altitudes = [0.0, 11000.0, 20000.0, 32000.0, 47000.0, 51000.0, 71000.0, 84852.0]
    staticpres= [101325.0, 22632.1, 5474.89, 868.02, 110.91, 66.94, 3.96, 0.3734]
    standtemp = [288.15, 216.65, 216.65, 228.65, 270.65, 270.65, 214.65, 186.87]
    lapserate = [-0.0065, 0.0, 0.001, 0.0028, 0.0, -0.0028, -0.002, 0.0]
    R = 8.31432
    g0 = 9.80665
    M = 0.0289644
    i = 8

    if alt <= altitudes[0]:
        press = 101325.0
        temp = 288.15
    elif alt > altitudes[0] and alt <= altitudes[1]:
        i=0
    elif alt <= altitudes[2]:
        i=1
    elif alt <= altitudes[3]:
        i=2
    elif alt <= altitudes[4]:
        i=3
    elif alt <= altitudes[5]:
        i=4
    elif alt <= altitudes[6]:
        i=5
    elif alt <= altitudes[7]:
        i=6
    else:
        press = 0.0
        temp = 186.87

    if i == 0 or i == 2 or i == 3 or i == 5 or i == 6:
        press = staticpres[i]*(standtemp[i]/(standtemp[i]+lapserate[i]*(alt-altitudes[i])))**(g0*M/(R*lapserate[i]))
        temp = standtemp[i]+lapserate[i]*(alt-altitudes[i])
    elif i == 1 or i == 4:
        press = staticpres[i]*math.exp((-g0*M*(alt-altitudes[i])/(R*standtemp[i])))
        temp = standtemp[i]+lapserate[i]*(alt-altitudes[i])

    dens = press/(287.058*temp)
    sspeed = math.sqrt(1.4*287.058*temp)

    return [press, temp, dens, sspeed]
