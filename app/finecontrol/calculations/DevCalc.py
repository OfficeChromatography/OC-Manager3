
import numpy as np
from scipy import interpolate

def speedSpline(x, y, steps):
    '''
    x: start and endposition in x
    y: Speed Coefficients consistent with x
    steps: will influence precision of the spline interpolation, high -> high precision
    '''
    x = np.array(np.linspace(x[0],x[1], len(y)))
    y = np.array(y)
    tck = interpolate.splprep( [x,y] ,s = 0 )
    xnew,ynew = interpolate.splev( np.linspace( 0, 1, steps), tck[0],der = 0)
    del xnew[-1]
    del ynew[-1]
    return xnew,ynew

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



