
import numpy as np
#from scipy import interpolate
from scipy.interpolate import CubicSpline

# def speedSpline(a1, a2, a3, a4, steps):
#     '''
#     values a1,a2,a3,a4: coefficients to create the bezier curve
#     steps: will influence precision of the spline interpolation, high -> high precision
#     '''
#     bezierfunc = lambda t: bezier(a1,a2,a3,a4,t)
#     t = np.delete(np.linspace(0, 1, steps+1), -1)
#     coordinates = list(map(bezierfunc,t))
#     return coordinates

def cubicSpline(data,steps):
    x = np.array([0,10,20,30,40,50,60,70,80,90,100])
    y = np.array(data)
    cs = CubicSpline(x,y)
    t = np.delete(np.linspace(0, 100, steps+1), -1)
    coordinates = list(map(cs,t))
    return coordinates

# def bezier(a1,a2,a3,a4,t):
#     #x =  (1 - t)**3 * 0 + 3 * (1 - t)**2 * t * 33 + 3 * (1 - t) * t**2 * 66 + t**3 * 100
#     y =  (1 - t)**3 * a1 + 3 * (1 - t)**2 * t * a2 + 3 * (1 - t) * t**2 * a3 + t**3 * a4
#     return y

def speedWeighting(speedList):
    '''weights the speed so that the volume of one band (the overall speed) stays constant, even if the speed is changing.'''
    integral = 0
    for entry in speedList:
        integral += entry/len(speedList)

    volCoefficient = 1/integral

    weightedSpeedList = [volCoefficient * x for x in speedList]

    return weightedSpeedList

def flowrate(length, speed, volume):
    time = length / speed
    flowrate = volume / time

    return flowrate



