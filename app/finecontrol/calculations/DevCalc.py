
import numpy as np
#from scipy import interpolate
from scipy.interpolate import CubicSpline

from types import SimpleNamespace

from finecontrol.gcode.GcodeGenerator import GcodeGenerator
from finecontrol.calculations.volumeToZMovement import volumeToZMovement

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

def calculateDevelopment(data):
    data = SimpleNamespace(**data)
    
    length = float(data.size_x)-float(data.offset_left)-float(data.offset_right)
    startPoint = [round(float(data.offset_left)+float(data.zero_x),3), round(float(data.offset_bottom)+float(data.zero_y),3)]
    
    zMovement = volumeToZMovement(data.volume,True)

    
    #speedSplineList = speedSpline(data.a1, data.a2, data.a3, data.a4, 10)
    speedSplineList = cubicSpline([data.a0, data.a1, data.a2, data.a3, data.a4, data.a5, data.a6, data.a7, data.a8, data.a9, data.a10],10)
    speedfactorList = speedWeighting(speedSplineList)

    #print(speedfactorList)
    return GcodeGenDevelopment(startPoint, length, zMovement, data.applications, data.printBothways, float(data.speed)*60, data.temperature, data.pressure, data.waitTime, speedfactorList)


def GcodeGenDevelopment(startPoint, length, zMovement, applications, printBothways, speed, temperature, pressure, waitTime, speedfactorList):
    generate = GcodeGenerator(True)

    # No HEATBED CASE
    if temperature != 0:
        generate.wait_bed_temperature(temperature)
        generate.hold_bed_temperature(temperature)
        generate.report_bed_temperature(4)
    
    # Move to the home
    generate.homming("XY")
    generate.linear_move_y(startPoint[1],speed)
    generate.linear_move_x(startPoint[0],speed)
    generate.finish_moves()
    #Set relative coordinates
    generate.set_relative()
    jj = 0   
    for x in range(int(applications)*2):
        #moving to the end of the line
        if (x%2)==0:
            generate.pressurize(pressure)
            generate.toggle_valve()
            for speedfactor in speedfactorList:
                generate.linear_move_xz(round(length/len(speedfactorList),3),round(zMovement*speedfactor/float(applications)/len(speedfactorList),3),speed)
            generate.toggle_valve()
            generate.check_pressure()
            generate.wait(waitTime)
            jj += 1
        #moving back to the start of the line
        else:
            if printBothways == 'On':
                generate.pressurize(pressure)
                generate.toggle_valve()
                for speedfactor in speedfactorList:
                    generate.linear_move_xz(-1*round(length/len(speedfactorList),3),round(zMovement*speedfactor/float(applications)/len(speedfactorList),3),speed)
                generate.toggle_valve()
                generate.check_pressure()
                generate.wait(waitTime)
                jj += 1
            else:
                generate.linear_move_x(-1*length,speed)
        if jj >= int(applications):
            break
    #Stop heating
    if (temperature !=0):
        generate.hold_bed_temperature(0)
        generate.report_bed_temperature(0)
    #set to absolute again
    generate.set_absolute()    
    #Homming
    generate.homming("XY")
    print(generate.list_of_gcodes)
    return generate.list_of_gcodes



