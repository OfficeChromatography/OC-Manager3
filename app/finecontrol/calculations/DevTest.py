from types import SimpleNamespace

def volumeToZMovement(volume, ul):
    '''
    if ul -> true:
    volume in ul -> zMovement in (mm)
    else:
    volume in ml -> zMovement in (mm)
    '''
    if ul:
        return round(40*float(volume)/3000,2)
    else:
        return round(40*float(volume)/3,2)

class GcodeGenerator:

    def __init__(self, save_in_list):
        self.list_of_gcodes = []
        self.save_in_list = save_in_list

    def check_return(self, gcode):
        if self.save_in_list:
            self.list_of_gcodes.append(gcode)
            return
        else:
            return gcode

    def linear_move_xyz(self, pos_x, pos_y, pos_z, speed):
        """"A linear move traces a straight line from one point to another, ensuring that the specified axes will arrive
        simultaneously at the given coordinates (by linear interpolation). The speed may change over time following an
        acceleration curve, according to the acceleration and jerk settings of the given axes."""
        if pos_x != "":
            pos_x = str(round(float(pos_x), 3))
        if pos_y != "":
            pos_y = str(round(float(pos_y), 3))
        if pos_z != "":
            pos_z = str(round(float(pos_z), 3))
        return self.check_return(f"G1X{pos_x}Y{pos_y}Z{pos_z}F{speed}")

    def linear_move_x(self, pos_x, speed):
        return self.linear_move_xyz(pos_x, "", "", speed)

    def linear_move_y(self, pos_y, speed):
        return self.linear_move_xyz("", pos_y, "", speed)

    def linear_move_z(self, pos_z, speed):
        return self.linear_move_xyz("", "", pos_z, speed)

    def linear_move_xy(self, pos_x, pos_y, speed):
        return self.linear_move_xyz(pos_x, pos_y, "", speed)

    def linear_move_xz(self, pos_x, pos_z, speed):
        return self.linear_move_xyz(pos_x, "", pos_z, speed)

    def linear_move_yz(self, pos_y, pos_z, speed):
        return self.linear_move_xyz("", pos_y, pos_z, speed)

    def wait_bed_temperature(self, temperature):
        """This command optionally sets a new target bed temperature and waits for the target temperature
        to be reached before proceeding. """
        return self.check_return(f"M190R{temperature}")

    def hold_bed_temperature(self, temperature):
        '''This command sets a new bed temperature and proceeds without waiting. The temperature will be held in the background'''
        return self.check_return(f"M140S{temperature}")

    def report_bed_temperature(self, timeIntervall):
        '''
        It can be useful for host software to track temperatures, display and graph them over time, but polling with M105 is less than optimal. 
        With M155 hosts simply set an interval and Marlin will keep sending data automatically. This method is preferred over polling with M105.
        timeIntervall in seconds
        '''
        return self.check_return(f"M155S{timeIntervall}")


    def homming(self, axis):
        """Auto-home one or more axes, moving them towards their endstops until triggered."""
        return self.check_return(f"G28{axis.upper()}")

    def set_position_xyz(self, pos_x, pos_y, pos_z):
        """Set the current position to the values specified."""
        return self.check_return(f"G92X{pos_x}Y{pos_y}Z{pos_z}")

    def set_position_x(self, pos_x):
        """Set the current position to the values specified."""
        return self.check_return(f"G92X{pos_x}")

    def set_position_y(self, pos_y):
        """Set the current position to the values specified."""
        return self.check_return(f"G92Y{pos_y}")

    def set_position_z(self, pos_z):
        """Set the current position to the values specified."""
        return self.check_return(f"G92Z{pos_z}")

    def set_position_xy(self, pos_x, pos_y):
        """Set the current position to the values specified."""
        return self.check_return(f"G92X{pos_x}Y{pos_y}")

    def set_position_xz(self, pos_x, pos_z):
        """Set the current position to the values specified."""
        return self.check_return(f"G92X{pos_x}Z{pos_z}")

    def set_position_yz(self, pos_y, pos_z):
        """Set the current position to the values specified."""
        return self.check_return(f"G92Y{pos_y}Z{pos_z}")

    def finish_moves(self):
        """This command causes G-code processing to pause and wait in a loop until all
        moves in the planner are completed."""
        return self.check_return(f"M400")

    def pressurize(self, pressure):
        """This command increase the pressure in the system"""
        return self.check_return(f"G97P{pressure}")

    def open_valve(self, frequency):
        """This command open and close the valve at a certain frequency"""
        return self.check_return(f"G98F{frequency}")

    def toggle_valve(self):
        """This command toggles the valve. 
        open -> close, close -> open"""
        return self.check_return(f"G40")

    def set_pin_state(self, pin, state):
        """For custom hardware not officially supported in Marlin, you can often just connect
        up an unused pin and use M42 to control it."""
        return self.check_return(f"M42P{pin}S{state}")
    
    def wait(self, time):
        """pauses the command queue and waits for a period of time in seconds"""
        return self.check_return(f"G4S{time}")
    
    def set_relative(self):
        """In this mode all coordinates are interpreted as relative to the last position."""
        return self.check_return(f"G91")

    def set_absolute(self):
        """In absolute mode all coordinates given in G-code are interpreted as positions in the logical coordinate space."""
        return self.check_return(f"G90")

    def check_pressure(self):
        return self.check_return(f"G95P")

    def rinsing(self):
        self.homming("XY")
        self.pressurize("60")
        self.open_valve("2")

    def set_new_zero_position(self, x, y,speed):
        self.homming("XY")
        self.linear_move_xy(x, y, speed)
        self.set_position_xy(0, 0)
        self.finish_moves()

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