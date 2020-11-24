def volumeToZMovement(volume):
    '''
    volume in ml -> zMovement in (mm)
    '''
    return round(30*float(volume)/2000,2)

def zMovementToVolume(zMovement):
    return round(float(zMovement)*2000/30,2)