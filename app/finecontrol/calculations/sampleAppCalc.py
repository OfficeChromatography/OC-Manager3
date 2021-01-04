import math
import json
import numpy as np
from scipy.optimize import minimize
from finecontrol.calculations.flowCalc import FlowCalc

def returnDropEstimateVol(data):
    working_area = [float(data.size_x)-float(data.offset_left)-float(data.offset_right)
    ,float(data.size_y)-float(data.offset_top)-float(data.offset_bottom)]
    if int(data.main_property)==1:
        n_bands = int(data.value)
        number_of_gaps = n_bands - 1
        sum_gaps_size = float(data.gap)*number_of_gaps
        length = (working_area[0]-sum_gaps_size)/n_bands
    else:
        length = data.value
        n_bands = int(math.trunc(working_area[0]/(float(length)+float(data.gap))))
        
    results = []
    for table in data.table:
        print1time = False
        dropVolume = FlowCalc(pressure=float(data.pressure), nozzleDiameter=data.nozzlediameter, timeOrFrequency = float(data.frequency), fluid=table['type'], density=table['density'], viscosity=table['viscosity']).calcVolumeFrequency()

        pointsX = np.round(float(length)/float(data.delta_x))+1
        pointsY = np.round(float(data.height)/float(data.delta_y))+1
        vol2 = (pointsX-1) * (pointsY-1) * dropVolume
        vol = pointsX * pointsY * dropVolume
        #print(vol,vol2)
        
        volPerBand = (table['volume (ul)'])
        if (volPerBand == "" or volPerBand == "null"):
            volPerBand = 0
            print1time = True
            
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
        
        if print1time:
            results.append([dropVolume, realVolume, 1, vol])
        else:
            results.append([dropVolume, realVolume, times, vol])

    return results
