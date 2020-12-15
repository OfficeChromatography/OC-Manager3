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
    

def zMovementToVolume(zMovement):
    return round(float(zMovement)*3000/40,2)

'''40 mm = 3ml'''