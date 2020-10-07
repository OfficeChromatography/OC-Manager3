import math
#from scipy.interpolate import interp2d

class FlowCalc:
    def __init__(self, pressure, nozzleDiameter, fluid, density, viscosity):
        '''
        density [g/cm^3]
        pressure [psi]
        nozzleDiameter ['0.xxmm']
        frequency [Hz]
        '''

        """density [g/cm**3] / kinematic viscosity [cSt] Correction Factor"""
        fluidDensity_empiricCorrectionFactor = {
            "Water": (1, 10),
            "Methanol": (0.792, 10),
            "Acetone": (0.784, 10),
            'n-Hexane': (0.655, 10),
            'Pentane': (0.6209, 10),
            'Cyclohexane': (0.779, 10),
            'Carbon Tetrachloride': (1.589, 10),
            'Toluene': (0.867, 10),
            'Chloroform': (1.49, 10),
            'Dichloromethane': (1.33, 10),
            'Diethyl ether': (0.713, 10),
            'Ethyl acetate': (0.902, 10),
            'Ethanol': (0.789, 10),
            'Pyridine': (0.982, 10)
        }

        if (fluid!='Specific'):
            [density, empiricCorrectionFactor] = fluidDensity_empiricCorrectionFactor[fluid]
        else:
            density = float(density)
            viscosity = float(viscosity)
            empiricCorrectionFactor = fluidDensity_empiricCorrectionFactor["Water"][1] / viscosity

        # self.time = time
        self.pressure = pressure
        self.density = density
        self.empiricCorrectionFactor = empiricCorrectionFactor
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

    def calcFlow(self):
        '''
        flowRateI [ul/s]
        '''
        unitConversionKonstantK = 75700.
        lohms= self.nozzleLohms + 4750 + 2600

        #flowrate in ul per s
        flowRateI = self.empiricCorrectionFactor * unitConversionKonstantK / lohms * math.sqrt( self.pressure / self.density ) / 60. * 1000
        return flowRateI

    # def calcVolume(self):
    #     '''
    #     calculates the volume for one opening of the valve
    #     volume [ul]
    #     '''
    #     volume = self.calcFlow() * self.time
    #     return volume



