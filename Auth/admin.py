from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,AuthDevice

admin.site.register(User, UserAdmin)

class AuthDeviceAdmin(admin.ModelAdmin):
    list_display = ("device_name","mac_addres")
    @admin.display(description='device name')
    def device_name(self, object):
        return object.device.name
admin.site.register(AuthDevice,AuthDeviceAdmin)
