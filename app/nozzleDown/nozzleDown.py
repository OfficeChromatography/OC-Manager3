import math;

class NozzleDown:
    def __init__(self,phialCoords,volume)
        self.distance = 5
        self.homeDistance = 100
        self.phialCoords = phialCoords
        self.volume = round(volume * 60/1000,3)
        self.speed = 10

    def nozzleDown(self):
        gcode = ['G90','G1E5']
        return gcode

    def nozzleUp(self):
        gcode = ['G90','G1E0']
        return gcode

    def nozzleHome(self):
        gcode = ['G41','G92E0']
        return gcode

    def loadFluid(self):
        gcode=[]
        #move to selected phial
        gcode.append(f'G1 X{self.phialCoords[0]} Y{self.phialCoords[1]}')
        #move nozzle down
        gcode.append(nozzleDown())
        #fill syringe
        gcode.append('G40',f'G1 Z-{self.volume} F{self.speed}','G40')
        #move nozzle up
        gcode.append(nozzleUp())
        
        return gcode
        
