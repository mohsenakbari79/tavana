from django.contrib import admin
from Devices.models import Device,Sensor,SensorForDevice
# Register your models here.

admin.site.register(Device)
admin.site.register(Sensor)
admin.site.register(SensorForDevice)



