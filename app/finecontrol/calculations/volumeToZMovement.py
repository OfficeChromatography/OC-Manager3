import os

SYRINGE_VOLUME = int(os.environ.get('SYRINGE_VOLUME'))
SYRINGE_LENGTH = int(os.environ.get('SYRINGE_LENGTH'))


def volumeToZMovement(volume, ul):
    """
    if ul -> true:
    volume in ul -> zMovement in (mm)
    else:
    volume in ml -> zMovement in (mm)
    """
    if ul:
        return round(SYRINGE_LENGTH * float(volume) / (SYRINGE_VOLUME * 1000), 2)
    else:
        return round(SYRINGE_LENGTH * float(volume) / SYRINGE_VOLUME, 2)


def zMovementToVolume(z_movement, ul):
    if ul:
        return round(float(z_movement) * SYRINGE_VOLUME * 1000 / SYRINGE_LENGTH, 2)
    else:
        return round(float(z_movement) * SYRINGE_VOLUME / SYRINGE_LENGTH, 2)


'''40 mm = 3ml'''
