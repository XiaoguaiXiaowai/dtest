from django.contrib import admin
from cmdb.models import Host

class HostAdmin(admin.ModelAdmin):
    list_display = ['host', 'ip', 'cpu', 'memory', 'disk', 'desc']
admin.site.register(Host, HostAdmin)
