from django.db import models
from django.contrib.auth import get_user_model
# Save the monitor text


class Monitor_Db(models.Model):
    monitortext = models.TextField(blank=True)

def __str__(self):
    return self.oc_lab
