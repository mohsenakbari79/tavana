from django.db import models
from django.contrib.auth.models import AbstractUser
import random



def create_new_ref_number():
      return random.randint(1000, 9999)


# Create your models here.
class AuthDevice(models.Model):
    token=models.IntegerField(default=create_new_ref_number,primary_key=True,unique=True)
    mac_addres=models.CharField(max_length=50,unique=True,blank=True,null=True)



# Create your models here.
class User(AbstractUser):
	email = models.EmailField(unique=True, verbose_name='آدرس ایمیل')
	class Meta:
		verbose_name = "کاربر"
		verbose_name_plural = "کاربران"
		ordering = ['-is_superuser']




