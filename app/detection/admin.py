from django.contrib import admin
from .models import Images_Db ,temporalImage
from django.db import models


admin.site.register(Images_Db)
admin.site.register(temporalImage)