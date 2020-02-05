from django.contrib import admin
from .models import Connection_Db


class Connection_DbAdmin(admin.ModelAdmin):
    readonly_fields = ('oc_lab', 'baudrate', 'timeout', 'time_of_connection',)


admin.site.register(Connection_Db, Connection_DbAdmin)
