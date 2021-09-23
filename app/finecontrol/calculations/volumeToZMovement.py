import os

SYRINGE_VOLUME = int(os.environ.get('SYRINGE_VOLUME'))
SYRINGE_LENGTH = int(os.environ.get('SYRINGE_LENGTH'))


def volumeToZMovement(volume, ul):
    '''
    if ul -> true:
    volume in ul -> zMovement in (mm)
    else:
    volume in ml -> zMovement in (mm)
    '''
    if ul:
        return round(SYRINGE_LENGTH * float(volume) / SYRINGE_VOLUME * 1000, 2)
    else:
        return round(SYRINGE_LENGTH * float(volume) / SYRINGE_VOLUME, 2)


def zMovementToVolume(zMovement, ul):
    if ul:
        return round(float(zMovement) * SYRINGE_VOLUME * 1000 / 40, 2)
    else:
        return round(float(zMovement) * SYRINGE_VOLUME / 40, 2)


'''40 mm = 3ml'''
