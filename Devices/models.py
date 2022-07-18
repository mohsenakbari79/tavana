from django.db import models
from django.core.exceptions import ValidationError
from Auth.models import AuthDevice
from django.core.validators import MaxValueValidator, MinValueValidator
from Auth.models import User 
# Create your models here.


class Device(models.Model):
    user = models.ForeignKey("Auth.User",on_delete=models.CASCADE,related_name="device_user") 
    name=models.CharField(max_length=50,blank=True,unique=True)
    versions=models.IntegerField(default=1,blank=True)
    release=models.FileField(upload_to ='release/',blank=True)
    auth=models.OneToOneField("Auth.AuthDevice",on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        auth_device=AuthDevice()
        auth_device.save()
        self.auth=auth_device
        super(Device, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}"
class Operators(models.Model):
    TYPE_CHOICES = (
        ("NUM", "number"),
        ("STR", "string"),
    )
    operator_type = models.CharField(max_length=4,choices=TYPE_CHOICES, default=1) 
    NAME_CHOICES = (
        ("eq", "equal"),
        ("gt", "greater"),
        ("lt", "lower"),
        ("ne", "difference"),
        ("ge", "greater and equal"),
        ("le", "lower and equal"),
    )
    operaror_name = models.CharField(max_length=2,choices=NAME_CHOICES)



class Sensor(models.Model):
    uniq_name = models.CharField(max_length=50,unique=True)
    pin_number = models.IntegerField(default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])
    def __str__(self):
        return f"{self.uniq_name}"

class Relay(models.Model):
    uniq_name = models.CharField(max_length=25)

class RelayForDevice(models.Model):
    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device,on_delete=models.CASCADE,related_name="device_relay")
    relay = models.ForeignKey(Relay,on_delete=models.CASCADE)
    enable = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.device.name} - {self.sensor.uniq_name}"
    class Meta:
        unique_together = ('device', 'id',)

class SensorValueType(models.Model):
    sensor = models.ForeignKey(Sensor,on_delete=models.CASCADE)
    sort = models.IntegerField(default=0)
    name = models.CharField(max_length=15) 
    TYPE_CHOICES = (
        ("Num", "Number"),
        ("STR", "string"),
    )
    types = models.CharField(max_length=4,choices=TYPE_CHOICES, default=1)   
    def __str__(self):
        return f"{self.name}"
    class Meta:
        unique_together = ('sensor', 'name',)


class SensorForDevice(models.Model):
    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device,on_delete=models.CASCADE,related_name="device_sensor")
    sensor = models.ForeignKey(Sensor,on_delete=models.CASCADE)
    enable = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.device.name} - {self.sensor.uniq_name}"
    class Meta:
        unique_together = ('device', 'id',)

class SensorDeviceValidation(models.Model):
    device_sensor = models.ForeignKey(SensorForDevice,on_delete=models.CASCADE,related_name="sensorvalidation")
    sort = models.IntegerField(default=0)
    senortype = models.ForeignKey("SensorValueType",on_delete=models.CASCADE)
    relay = models.ForeignKey("RelayForDevice",on_delete=models.CASCADE)
    operator = models.ForeignKey("Operators",on_delete=models.CASCADE)
    operator_value = models.CharField(max_length=40)
    CHOISE_FIELD = (
        (0 , "enable"),
        (1 , "disable"),
    )
    active = models.IntegerField(default=0,choices=CHOISE_FIELD)
    def save(self, *args, **kwargs):
        super(SensorValueType, self).save(*args, **kwargs)
    def __str__(self):
        return f"{self.device_sensor.device.name} - {self.device_sensor.sensor.uniq_name}"
    

    



class PinOfDevice(models.Model):
    device = models.OneToOneField(Device,on_delete=models.CASCADE,primary_key = True)
    pin_number = models.IntegerField(default=10,editable=False)
    pin = models.JSONField(blank=True) # serialized custom data
    def save(self, *args, **kwargs):
        if self.pin==None:
            temp={}
            for pin_num in range(self.pin_number):
                temp[pin_num]=None
            self.pin=temp
        super(PinOfDevice, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.device.name} - {self.pin_number}"
    @property
    def pin_dict(self):
        return simplejson.loads(self.pin)

class TimeEnable(models.Model):
    sensorfordevice=models.ForeignKey("SensorForDevice",on_delete=models.CASCADE,related_name="time_enable")
    start_day=models.DateField(null=True,blank=True)
    end_day=models.DateField(blank=True)
    start_time=models.TimeField(blank=True)
    end_time=models.TimeField(blank=True)
    def save(self, *args, **kwargs):
        all_time=TimeEnable.objects.filter(sensorfordevice=self.sensorfordevice)
        if (self.end_day != None and self.start_day < self.end_day) or (self.end_time != None and self.start_time < self.end_time):
            pass
        for time_check in all_time:          
            if self.start_day != None and self.end_day != None and\
                    time_check.start_day != None and time_check.start_day != None and  \
                    (time_check.start_day < d2.start_day < time_check.end_day) or (time_check.start_day < d2.end_day < time_check.end_day) or (d2.start_day <= time_check.start_day and d2.end_day >= time_check.end_day):       
                if self.start_time != None and self.end_time != None and\
                    time_check.start_time != None and time_check.start_time != None and  \
                    (time_check.start_time < d2.start_time < time_check.end_time) or (time_check.start_time < d2.end_time < time_check.end_time) or (d2.start_time <= time_check.start_time and d2.end_time >= time_check.end_time):
                    raise ValidationError()  
                
        super(TimeEnable, self).save(*args, **kwargs)    
