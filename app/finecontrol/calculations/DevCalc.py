from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate



# x = np.array([0,25,50,75,100])
# y = np.array([1,1.5,1.5,1,1])

# tck,u     = interpolate.splprep( [x,y] ,s = 0 )
# xnew,ynew = interpolate.splev( np.linspace( 0, 1, 10 ), tck,der = 0)
def speedSpline(x, y, steps):
    '''
    x: Position in x
    y: Speed Coefficients consistent with x
    steps: will influence precision of the spline interpolation, high -> high precision
    '''
    tck = interpolate.splprep( [x,y] ,s = 0 )
    xnew,ynew = interpolate.splev( np.linspace( 0, 1, steps), tck,der = 0)
    return xnew,ynew

def speedWeighting(speedList):
    '''weights the speed so that the volume of one band (the overall speed) stays constant, even if the speed is changing.'''
    integral = 0
    for entry in speedList:
        integral += entry/len(speedList)

    volCoefficient = 1/integral

    weightedSpeedList = [volCoefficient * x for x in speedList]

    return weightedSpeedList




