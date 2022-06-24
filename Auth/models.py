from django.db import models
import random
def create_new_ref_number():
      return random.randint(1000000000, 9999999999)


# Create your models here.
class AuthDevice(models.Model):
    token=models.IntegerField(default=create_new_ref_number,primary_key=True,unique=True)
    mac_addres=models.CharField(max_length=50,unique=True,blank=True,null=True)


