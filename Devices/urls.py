from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = 'devices'

router = routers.DefaultRouter()

router.register(r'device_models', DeviceModelsViewSet, basename='deviceModels')
router.register(r'device', DeviceViewSet, basename='device')
router.register(r'pin', PinForDeviceViewSet, basename='pin')
router.register(r'sensor', SensorViewSet, basename='sensor')
router.register(r'relay', RelayViewSet, basename='relay')
router.register(r'sensor_device', SensorForDeviceViewSet, basename='sensor_device')
router.register(r'relay_device', RelayForDeviceViewSet, basename='relay_device')
router.register(r'value_sensor', SensorValueTypeViewSet, basename='value_sensor')

router.register(r'time_device', TimeDefualtValueViewSet, basename='time_device')
router.register(r'operators', OperatorsViewSet, basename='operators')
router.register(r'validations_sensore', SensorDeviceValidationViewSet, basename='validation_device')

router.register(r'time_action', TimeActionViewSet, basename='time_action')



urlpatterns = [
	path('api/', include(router.urls)),
	path('api/value/sensor/<str:device>',sensorvalue,name="senosrvalue"),
	path('api/value/sensor/<str:device>/<str:sensore>',sensorvalue,name="senosrvalueall"),
	path('api/tasksname/',tasksname,name="tasksname"),
]
