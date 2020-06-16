from django.contrib import admin
from .models import PlateProperties_Db, BandSettings_Db, MovementSettings_Db, PressureSettings_Db, SampleApplication_Db, BandsComponents_Db
from django.db import models

admin.site.register(PlateProperties_Db)
admin.site.register(BandSettings_Db)
admin.site.register(MovementSettings_Db)
admin.site.register(BandsComponents_Db)



admin.site.register(PressureSettings_Db)
admin.site.register(SampleApplication_Db)
