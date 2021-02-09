import math
import json
import numpy as np
from scipy.optimize import minimize
from finecontrol.calculations.flowCalc import FlowCalc
from types import SimpleNamespace
from finecontrol.gcode.GcodeGenerator import GcodeGenerator


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

        dropVolume = FlowCalc(pressure=float(data.pressure), nozzleDiameter=data.nozzlediameter, timeOrFrequency = float(data.frequency), fluid=table['type'], density=table['density'], viscosity=table['viscosity']).calcVolumeFrequency()

        pointsX = np.round(float(length)/float(data.delta_x))+1
        pointsY = np.round(float(data.height)/float(data.delta_y))+1
        vol2 = (pointsX-1) * (pointsY-1) * dropVolume
        vol = pointsX * pointsY * dropVolume
        #print(vol,vol2)
        
        volPerBand = (table['volume'])
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
        
        values = {  "estimated_volume": realVolume,
                    "estimated_drop_volume": dropVolume,
                    "times": times,
                    "minimum_volume": vol}
        results.append(values)
    return results

def minusOneUntilZero(number):
    number = number -1
    if number < 0: number = 0
    return number


def calculate(data):

    data = SimpleNamespace(**data)

    working_area = [data.size_x-data.offset_left-data.offset_right,data.size_y-data.offset_top-data.offset_bottom]

    if data.main_property==1:
        n_bands = int(data.value)
        number_of_gaps = n_bands - 1
        sum_gaps_size = data.gap*number_of_gaps
        length = (working_area[0]-sum_gaps_size)/n_bands
    else:
        length = data.value
        n_bands = int(math.trunc(working_area[0]/(length+data.gap)))


    volEstimate = returnDropEstimateVol(data)
    #print(returnDropEstimateVol(data))
    sampleTimes = [d['times'] for d in volEstimate]
    
    
    list_of_bands = []

    deltaX = float(data.delta_x)
    deltaY = float(data.delta_y)
    j = 0
    while sum(sampleTimes)!=0:
        for i in range(0,n_bands):
            if sampleTimes[i]==0: continue
            bandlist = []
            zeros=(i*(length+data.gap))+data.offset_left
            if j % 2:
                current_height = deltaY/2
                while current_height <= data.height:
                    applicationline=[]
                    current_length=deltaX/2
                    while current_length<=length:
                        applicationline.append([current_length+float(zeros), float(data.offset_bottom)+current_height])
                        current_length+=deltaX
                    bandlist.append(applicationline)
                    current_height+=deltaY
            else:
                current_height = 0.
                while current_height <= data.height:
                    applicationline=[]
                    current_length=0.
                    while current_length<=length:
                        applicationline.append([current_length+float(zeros), float(data.offset_bottom)+current_height])
                        current_length+=deltaX
                    bandlist.append(applicationline)
                    current_height+=deltaY
            list_of_bands.append(bandlist)
        j += 1
        sampleTimes = list(map(minusOneUntilZero,sampleTimes))
        #print(sampleTimes)

    # Creates the Gcode for the application and return it
    return gcode_generation(list_of_bands, data.motor_speed, data.frequency, data.temperature, data.pressure, [data.zero_x,data.zero_y])


def gcode_generation(list_of_bands, speed, frequency, temperature, pressure, zeroPosition):
    generate = GcodeGenerator(True)

    # No HEATBED CASE
    if temperature != 0:
        generate.wait_bed_temperature(temperature)
        generate.hold_bed_temperature(temperature)
        generate.report_bed_temperature(4)

    # Move to the home
    # generate.set_new_zero_position(zeroPosition[0], zeroPosition[1], speed)

    # Application
    # generate.pressurize(pressure)
    
    generate.rinsing()
    generate.set_new_zero_position(zeroPosition[0], zeroPosition[1], speed)
    jj = 0
    for band in list_of_bands:
        for index, list_of_points in enumerate(band):
            if jj > 50:
                generate.rinsing()
                generate.set_new_zero_position(zeroPosition[0], zeroPosition[1], speed)
                jj = 0
            for point in list_of_points:
                generate.linear_move_xy(point[0], point[1], speed)
                generate.finish_moves()
                generate.pressurize(pressure)
                generate.open_valve(frequency)
                generate.finish_moves()
                jj += 1
    #Stop heating
    if (temperature !=0):
        generate.hold_bed_temperature(0)
        generate.report_bed_temperature(0)
    #Homming
    generate.homming("XY")
    #print(generate.list_of_gcodes)
    return generate.list_of_gcodes
