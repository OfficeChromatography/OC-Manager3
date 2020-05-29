from django.db import models
from django.contrib.auth import get_user_model

class GcodeFile(models.Model):
    filename = models.CharField(max_length=100, null=True)
    uploader = models.ForeignKey(
                get_user_model(),
                null=True,
                on_delete=models.CASCADE,
                blank=True,
                )
    gcode = models.FileField(null=True)
    gcode_url = models.CharField(max_length=100, null=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True)
