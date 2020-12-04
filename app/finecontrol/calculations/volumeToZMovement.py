def volumeToZMovement(volume):
    '''
    volume in ml -> zMovement in (mm)
    '''
    return round(40*float(volume)/3000,2)

def zMovementToVolume(zMovement):
    return round(float(zMovement)*3000/40,2)

'''40 mm = 3ml