#from finecontrol.gcode import GcodeGenerator
#from sampleapp.views import calculate
from types import SimpleNamespace
import math
import json
import numpy as np
from scipy.optimize import minimize

class FlowCalc:
    def __init__(self, pressure, nozzleDiameter, timeOrFrequency, fluid, density, viscosity):
        '''
        density [g/cm^3]
        pressure [psi]
        nozzleDiameter ['0.xxmm']
        timeOrFrequency [s] or [Hz]
            used in sample app as frequency [Hz]
            used in development as time [s]
        '''

        """density [g/cm**3]"""
        densityTable = {
            "Water": 1,
            "Methanol": 0.792,
            "Acetone": 0.784,
            'n-Hexane': 0.655,
            'Pentane': 0.6209,
            'Cyclohexane': 0.779,
            'Carbon Tetrachloride': 1.589,
            'Toluene': 0.867,
            'Chloroform': 1.49,
            'Dichloromethane': 1.33,
            'Diethyl ether': 0.713,
            'Ethyl acetate': 0.902,
            'Ethanol': 0.789,
            'Pyridine': 0.982,
        }
        if (fluid!='Specific'):
            fluidDensity= densityTable[fluid]
        else:
            fluidDensity = float(density)
            viscosity = float(viscosity)
            

        self.pressure = pressure
        self.timeOrFrequency = timeOrFrequency
        self.density = fluidDensity
        if nozzleDiameter=='0.25':
            self.nozzleLohms=7500.
        elif nozzleDiameter=='0.19':
            self.nozzleLohms=15400.
        elif nozzleDiameter=='0.13':
            self.nozzleLohms=35000.
        elif nozzleDiameter=='0.10':
            self.nozzleLohms = 60000.
        elif nozzleDiameter=='0.08':
            self.nozzleLohms = 125000.
        elif nozzleDiameter=='0.05':
            self.nozzleLohms = 280000.
        elif nozzleDiameter=='atomizer':
            self.nozzleLohms = 22000

    def calcFlow(self):
        '''
        flowRateI [ul/s]
        '''
        unitConversionKonstantK = 75700.
        lohms= math.sqrt(self.nozzleLohms**2 + 4750**2 + 2600**2)

        #empiricly determined correctionfactor
        correctionFactor = 5
        #flowrate in ul per s
        flowRateI = correctionFactor * unitConversionKonstantK / lohms * math.sqrt( self.pressure / self.density ) / 60. * 1000
        return flowRateI

    def calcVolumeFrequency(self):
        '''
        calculates the volume for one opening of the valve
        volume [ul] (SampleApp)
        '''
        volume = self.calcFlow() * (0.5 / self.timeOrFrequency)
        return volume
    
    def calcVolumeTime(self):
        '''
        calculates the volume for the valve opened for a duration of time
        (development)
        '''
        volume = self.calcFlow() * self.timeOrFrequency
        return volume

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
        
        volPerBand = (table['volume (ul)'])
        if (volPerBand == "" or volPerBand == "null"): #will apply 1 time if nothing is specified
            results.append([0, 0, 1, 0])
            continue
            
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
        
        
        results.append([dropVolume, realVolume, times, vol])

    return results


def calculate(data):

    data = SimpleNamespace(**data)

    working_area = [data.size_x-data.offset_left-data.offset_right,data.size_y-data.offset_top-data.offset_bottom]
    #print(working_area)

    if data.main_property==1:
        n_bands = int(data.value)
        number_of_gaps = n_bands - 1
        sum_gaps_size = data.gap*number_of_gaps
        length = (working_area[0]-sum_gaps_size)/n_bands
        #print(working_area[0],sum_gaps_size,length)
    else:
        length = data.value
        n_bands = int(math.trunc(working_area[0]/(length+data.gap)))


    volEstimate = returnDropEstimateVol(data)
    #print(volEstimate)
    list_of_bands = []
    
    deltaX = float(data.delta_x)
    deltaY = float(data.delta_y)
    for i in range(0,n_bands):
        bandlist = []
        zeros=(i*(length+data.gap))+data.offset_left
        for j in range(volEstimate[i][2]):
            if j % 2:
                current_height = deltaY/2
                while current_height <= data.height:
                    applicationline=[]
                    current_length=deltaX/2
                    while current_length<=length:
                        applicationline.append([float(data.offset_bottom)+current_height, current_length+float(zeros)])
                        current_length+=deltaX
                    bandlist.append(applicationline)
                    current_height+=deltaY
            else:
                current_height = 0.
                while current_height <= data.height:
                    applicationline=[]
                    current_length=0.
                    while current_length<=length:
                        applicationline.append([float(data.offset_bottom)+current_height, current_length+float(zeros)])
                        current_length+=deltaX
                    bandlist.append(applicationline)
                    current_height+=deltaY
        list_of_bands.append(bandlist)
        #print(list_of_bands)

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
    
    for band in list_of_bands:
        generate.rinsing()
        generate.set_new_zero_position(zeroPosition[0], zeroPosition[1], speed)
        jj = 0
        for index, list_of_points in enumerate(band):
            
            for point in list_of_points:
                generate.linear_move_xy(point[1], point[0], speed)
                generate.finish_moves()
                generate.pressurize(pressure)
                generate.open_valve(frequency)
                generate.finish_moves()
                jj += 1
                if jj > 50:
                    generate.rinsing()
                    generate.set_new_zero_position(zeroPosition[0], zeroPosition[1], speed)
                    jj = 0
    #Stop heating
    if (temperature !=0):
        generate.hold_bed_temperature(0)
        generate.report_bed_temperature(0)
    #Homming
    generate.homming("XY")
    return generate.list_of_gcodes

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
        self.open_valve("1")

    def set_new_zero_position(self, x, y,speed):
        self.homming("XY")
        self.linear_move_xy(x, y, speed)
        self.set_position_xy(0, 0)
        self.finish_moves()


data = {
    'size_x': 100, 
    'size_y': 100, 
    'offset_left': 2.5, 
    'offset_right': 2.5,
    'offset_top': 5, 
    'offset_bottom': 5, 
    'main_property': 1, 
    'value': 1, 
    'height': 0, 
    'gap': 0, 
    'motor_speed': 1000, 
    'delta_x': 2, 
    'delta_y': 1.5, 
    'pressure': 5, 
    'frequency': 1400,
    'temperature': 0, 
    'nozzlediameter': '0.08', 
    'zero_x': 5, 
    'zero_y': 18, 
    'table': [{'band': '1', 'description': '', 'volume (ul)': '', 'type': 'Water', 'density': '', 'viscosity': ''}]
    }

xlabel = "frequency"
xlist = range(600,1500,200)

ylabel = "pressure"
ylist = range(5,45,5)

offset = 2.5

listgcode = []
for idx,x in enumerate(xlist):
    data['offset_left'] = offset + idx*100/len(xlist) # 2.5 34.16 65,83
    data['offset_right'] = 100-(idx+1)*100/len(xlist) + offset
    data[xlabel] = x
    for idx2,y in enumerate(ylist):
        data['offset_bottom'] = 5 + idx2*5
        data[ylabel] = y
        gcode = calculate(data)
        listgcode.extend(gcode)

with open('SampleAppTest.txt', 'w') as f:
    for item in listgcode:
        f.write("%s\n" % item)
