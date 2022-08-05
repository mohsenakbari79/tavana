from django.contrib import admin
from Devices.models import (
    Device,
    Sensor,
    SensorForDevice,
    PinOfDevice,
    SensorValueType,
    # TimeEnable,
    Operators,
    SensorDeviceValidation,
    # TimeAction,
    DeviceModels,
    
)
# Register your models here.
class DeviceCodesAdmin(admin.ModelAdmin):
    exclude = ('auth',)

class DeviceModelsAdmin(admin.ModelAdmin):
    list_display = ("name","versions")
admin.site.register(DeviceModels,DeviceModelsAdmin)


class DeviceAdmin(admin.ModelAdmin):
    list_display = ("user_username","name")
    @admin.display(description='user name')
    def user_username(self, object):
        return object.user.username
        
    @admin.display(description='device models')
    def deviceModel_name(self, object):
        return object.deviceModel.name
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

# class TimeEnableTypeAdmin(admin.ModelAdmin):
#     list_display = ("start_day","end_day","start_time","end_time")
# admin.site.register(TimeEnable,TimeEnableTypeAdmin)



class OperatorsAdmin(admin.ModelAdmin):
    list_display = ("operator_type","operaror_name")
admin.site.register(Operators,OperatorsAdmin)


class SensorDeviceValidationAdmin(admin.ModelAdmin):
    list_display = ("sensor_uniq_name","relay","operator","active")
    @admin.display(description='sensor uniq_name ')
    def sensor_uniq_name(self, object):
        return object.device_sensor.senosr.uniq_name
admin.site.register(SensorDeviceValidation,SensorDeviceValidationAdmin)





# admin.site.register(TimeAction)