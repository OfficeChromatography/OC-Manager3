import os

SYRINGE_VOLUME = float(os.environ.get('SYRINGE_VOLUME'))
SYRINGE_LENGTH = float(os.environ.get('SYRINGE_LENGTH'))


def volume_to_z_movement(volume, ul):
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
