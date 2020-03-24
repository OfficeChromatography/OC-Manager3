from django.db import models
from django.contrib.auth import get_user_model
# To have a better understandig on the Fields of the Database read pySerial
# documentation. Mostly just the "class serial.Serial" parameters


class Monitor_Db(models.Model):
    monitortext = models.TextField(blank=True)

def __str__(self):
    return self.oc_lab
