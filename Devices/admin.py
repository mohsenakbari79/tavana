from django.contrib import admin
from Devices.models import Device,Sensor,SensorForDevice,PinOfDevice,SensorValueType,TimeEnable
# Register your models here.
class DeviceCodesAdmin(admin.ModelAdmin):
    exclude = ('auth',)

class DeviceAdmin(admin.ModelAdmin):
    list_display = ("user_username","name","versions")
    @admin.display(description='user name')
    def user_username(self, object):
        return object.user.username
admin.site.register(Device,DeviceAdmin)

class SensorAdmin(admin.ModelAdmin):
    list_display = ("uniq_name","pin_number")
admin.site.register(Sensor,SensorAdmin)

class SensorForDeviceAdmin(admin.ModelAdmin):
    list_display = ("device","sensor","enable")
admin.site.register(SensorForDevice,SensorForDeviceAdmin)

class PinOfDeviceAdmin(admin.ModelAdmin):
    list_display = ("device_name","pin_number")
    @admin.display(description='device name')
    def device_name(self, object):
        return object.device.name
admin.site.register(PinOfDevice,PinOfDeviceAdmin)

class SensorValueTypeAdmin(admin.ModelAdmin):
    list_display = ("sensor_uniq_name","types")
    @admin.display(description='sensor uniq_name ')
    def sensor_uniq_name(self, object):
        return object.sensor.uniq_name
admin.site.register(SensorValueType,SensorValueTypeAdmin)

class TimeEnableTypeAdmin(admin.ModelAdmin):
    list_display = ("start_day","end_day","start_time","end_time")
admin.site.register(TimeEnable,TimeEnableTypeAdmin)


