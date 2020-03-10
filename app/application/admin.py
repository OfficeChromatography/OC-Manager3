from django.contrib import admin
from .models import SampleApplication_Db, BandSettings_Db, PlateProperties_Db
from django.db import models


admin.site.register(SampleApplication_Db)
admin.site.register(BandSettings_Db)
admin.site.register(PlateProperties_Db)
