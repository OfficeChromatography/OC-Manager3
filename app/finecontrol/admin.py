from django.contrib import admin
from .models import GcodeFile

class GcodeFileAdmin(admin.ModelAdmin):
    pass
admin.site.register(GcodeFile, GcodeFileAdmin)
