from django.contrib import admin
from .models import BandSettings_Dev_Db, Development_Db, PlateProperties_Dev_Db, PressureSettings_Dev_Db
from django.db import models

admin.site.register(PlateProperties_Dev_Db)
admin.site.register(PressureSettings_Dev_Db)
admin.site.register(BandSettings_Dev_Db)
admin.site.register(Development_Db)
