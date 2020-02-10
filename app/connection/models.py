from django.db import models

# To have a better understandig on the Fields of the Database read pySerial
# documentation. Mostly just the "class serial.Serial" parameters

class Connection_Db(models.Model):
    oc_lab              = models.CharField(max_length=120)
    baudrate            = models.DecimalField(decimal_places=0, max_digits=6)
    timeout             = models.DecimalField(decimal_places=0, max_digits=4)
    time_of_connection  = models.DateTimeField(auto_now_add=True)
    chattext            = models.TextField(blank=True)
