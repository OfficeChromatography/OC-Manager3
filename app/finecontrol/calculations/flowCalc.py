import math
#from scipy.interpolate import interp2d

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