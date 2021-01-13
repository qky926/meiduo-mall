from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class user(AbstractUser):
    mobile = models.CharField(max_length=11,unique=True,verbose_name='手机号')

    def __str__(self):
        return self.username