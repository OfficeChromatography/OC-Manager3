from types import SimpleNamespace
from finecontrol.gcode import GcodeGenerator
from finecontrol.calculations.volumeToZMovement import volumeToZMovement


def calculateDevelopment(data):
    data = SimpleNamespace(**data)
    
    length = float(data.size_x)-float(data.offset_left)-float(data.offset_right)
    startPoint = [round(float(data.offset_left)+float(data.zero_x),3), round(float(data.offset_bottom)+float(data.zero_y),3)]
    
    zMovement = volumeToZMovement(data.volume,True)

    
    #speedSplineList = speedSpline([startPoint[0],startPoint[0]+length], [1,1,1],10)
    
    #speedfactorList = speedWeighting(speedSplineList[1])
    speedfactorList = speedWeighting([1,1,1])

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
            generate.open_valve()
            for speedfactor in speedfactorList:
                generate.linear_move_xz(round(length/len(speedfactorList),3),round(zMovement*speedfactor/float(applications)/len(speedfactorList),3),speed)
            generate.close_valve()
            generate.check_pressure()
            generate.wait(waitTime)
            jj += 1
        #moving back to the start of the line
        else:
            if printBothways == 'On':
                generate.pressurize(pressure)
                generate.open_valve()
                for speedfactor in speedfactorList:
                    generate.linear_move_xz(-1*round(length/len(speedfactorList),3),round(zMovement*speedfactor/float(applications)/len(speedfactorList),3),speed)
                generate.close_valve()
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
    
    print(generate.list_of_gcodes)
    return generate.list_of_gcodes

def flowrate(length, speed, volume):
    time = length / speed
    flowrate = volume / time

    return flowrate

def speedWeighting(speedList):
    '''weights the speed so that the volume of one band (the overall speed) stays constant, even if the speed is changing.'''
    integral = 0
    for entry in speedList:
        integral += entry/len(speedList)

    volCoefficient = 1/integral

    weightedSpeedList = [volCoefficient * x for x in speedList]

    return weightedSpeedList

data = {
    'size_x': 100, 
    'size_y': 100, 
    'offset_left': 1, 
    'offset_right': 1, 
    'offset_top': 1, 
    'offset_bottom': 2, 
    'temperature': 0, 
    'nozzlediameter': '0.08', 
    'pressure': 10, 
    'speed': 25, 
    'zero_x': 5, 
    'zero_y': 18, 
    'fluid': 'Methanol', 
    'printBothways': 'Off', 
    'volume': '100.0', 
    'density': '', 
    'viscosity': '', 
    'applications': '1', 
    'waitTime': '0', 
    'description': '123'
    }

xlabel = "speed"
xlist = range(10,40,5)


listgcode = []
for idx,x in enumerate(xlist):
    #data['offset_bottom'] = 5 + idx*10
    data['offset_bottom'] = (idx+1) * 100/(len(xlist)+1)
    data[xlabel] = x
    gcode = calculateDevelopment(data)
    listgcode.extend(gcode)
        

with open('DevTest.gcode', 'w') as f:
    for item in listgcode:
        f.write("%s\n" % item)
