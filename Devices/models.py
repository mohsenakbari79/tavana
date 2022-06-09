from django.db import models

# Create your models here.


class Device(models.Model):
    name=models.CharField(max_length=50,blank=True)
    versions=models.IntegerField(default=1,blank=True)
    release=models.FileField(upload_to ='release/',blank=True)


class Sensor(models.Model):
    uniq_name=models.CharField(max_length=50,unique=True)
    

class SensorForDevice(models.Model):
    device = models.ForeignKey(Device,on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor,on_delete=models.CASCADE)
    enable = models.BooleanField(default=True)
    value=models.JSONField(null=True,blank=True)

    class Meta:
        unique_together = ('device', 'sensor',)


