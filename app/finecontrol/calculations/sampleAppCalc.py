import math
import json
import numpy as np
from scipy.optimize import minimize
from finecontrol.calculations.flowCalc import FlowCalc

# def calculateDeltaX(length,height,maxPoints):
#     '''calculates the distance of the points if deltaX == deltaY'''

#     #deltaX = [0,0]
#     deltaX = - ((length+height)/(2*(1-maxPoints))) + math.sqrt(((length+height)/(2*(1-maxPoints)))**2-((length*height)/(1-maxPoints)))
#     #deltaX[1] = - ((length+height)/(2*(1-maxPoints))) - math.sqrt(((length+height)/(2*(1-maxPoints)))**2-((length*height)/(1-maxPoints)))

#     return deltaX

# def optimizeMaxPoints(length, height, maxPoints):
#     '''calculates the error function, so it can
#     be minimized to get the best number of points'''

#     deltaX = calculateDeltaX(length,height,maxPoints)
#     pointsX = np.round(length / deltaX)
#     pointsY = np.round(height / deltaX)

#     error = (pointsX * deltaX - length)**2 + (pointsY * deltaX - height)**2

#     return error

# def minimizeDeltaX(length, height, volume, bandNum, data):
#     '''calculates deltaX according to the set volume'''
#     #print(data)
#     dropVolume = FlowCalc(pressure=float(data.pressure), nozzleDiameter=data.nozzlediameter, timeOrFrequency = float(data.frequency), fluid=data.table[bandNum]['type'], density=data.table[bandNum]['density'], viscosity=data.table[bandNum]['viscosity']).calcVolumeFrequency()
#     print("dropVolume: "+str(dropVolume))
#     #dropVolume = 0.025

#     optimizeTest = lambda maxPoints: optimizeMaxPoints(length, height, maxPoints)
#     x0 = volume / dropVolume
#     res = minimize(optimizeTest,x0)
#     points = np.round(res.x)
#     deltaX = calculateDeltaX(length,height,points)
#     realVolume = points * dropVolume

#     return [deltaX[0], realVolume]

def returnDropEstimateVol(data):
    #print(data)
    working_area = [float(data.size_x[0])-float(data.offset_left[0])-float(data.offset_right[0]),float(data.size_y[0])-float(data.offset_top[0])-float(data.offset_bottom[0])]
    if int(data.main_property[0])==1:
        n_bands = int(data.value[0])
        number_of_gaps = n_bands - 1
        sum_gaps_size = float(data.gap[0])*number_of_gaps
        length = (working_area[0]-sum_gaps_size)/n_bands
    else:
        length = data.value[0]
        n_bands = int(math.trunc(working_area[0]/(float(length)+float(data.gap[0]))))
        

    dataTable = json.loads(data.table[0])
    results = []
    for table in dataTable:

        dropVolume = FlowCalc(pressure=float(data.pressure[0]), nozzleDiameter=data.nozzlediameter[0], timeOrFrequency = float(data.frequency[0]), fluid=table['type'], density=table['density'], viscosity=table['viscosity']).calcVolumeFrequency()

        pointsX = np.round(float(length)/float(data.delta_x[0]))+1
        print(length)
        pointsY = 1
        vol2 = (pointsX-1) * dropVolume
        if data.height[0] != "0":
            pointsY = np.round(float(data.height[0])/float(data.delta_y[0]))+1
            vol2 = (pointsX-1) * (pointsY-1) * dropVolume
        vol = pointsX * pointsY * dropVolume
        print(vol,vol2)
        
        
        volPerBand = (table['volume (ul)'])
        if (volPerBand == "" or volPerBand == "null"):
            volPerBand = 0
        volPerBand = float(volPerBand)

        times = 0
        realVolume = 0
        dif = volPerBand - realVolume
        while dif >= 0:
            if times % 2:
                realVolume += vol2
            else:
                realVolume += vol
            dif = volPerBand - realVolume
            times += 1
        if times % 2:
            if abs(dif)>vol/2: 
                times -= 1
                realVolume -= vol
        else:
            if abs(dif)>vol2/2: 
                times -= 1
                realVolume -= vol2
            

        # times = round(float(volPerBand) / realVolume)
        # realVolume *= times

        #np.append(results, [dropVolume, realVolume])
        results.append([dropVolume, realVolume, times])

    return results
