from django.contrib import admin
from Devices.models import Device,Sensor,SensorForDevice,PinOfDevice
# Register your models here.
class DeviceCodesAdmin(admin.ModelAdmin):
    exclude = ('auth',)
admin.site.register(Device,DeviceCodesAdmin)
admin.site.register(Sensor)
admin.site.register(SensorForDevice)
admin.site.register(PinOfDevice)




