from django.contrib import admin
from .models import *
from django.db import models

admin.site.register(Derivatization_Db)
admin.site.register(PlateProperties_Db)
admin.site.register(ZeroPosition_Db)
admin.site.register(PressureSettings_Der_Db)
admin.site.register(BandSettings_Der_Db)
