from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = 'devices'

router = routers.DefaultRouter()
router.register(r'device', DeviceViewSet, basename='device')
router.register(r'pin', PinForDeviceViewSet, basename='pin')
router.register(r'sensor', SensorViewSet, basename='pin')
router.register(r'sensor_device', SensorForDeviceViewSet, basename='pin')




SensorViewSet



urlpatterns = [
	path('api/', include(router.urls)),
]