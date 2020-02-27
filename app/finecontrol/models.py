from django.db import models

class GcodeFile(models.Model):
    filename = models.CharField(max_length=100)
    uploader = models.CharField(max_length=100)
    gcode = models.FileField(upload_to = 'gcode/files', max_length = 100)
