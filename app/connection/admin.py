from django.contrib import admin
from .models import Connection_Db
from django.forms import Textarea
from django.db import models

class Connection_DbAdmin(admin.ModelAdmin):
    fields = ('id','oc_lab', 'username','baudrate', 'timeout', 'time_of_connection', 'chattext')
    readonly_fields = ('id','oc_lab', 'username','baudrate', 'timeout', 'time_of_connection')
    formfield_overrides = {models.TextField: dict(widget=Textarea(attrs=dict(readonly=True, cols=200, rows=20)))}


admin.site.register(Connection_Db, Connection_DbAdmin)
