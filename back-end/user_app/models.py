from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    # name = models.CharField() 
    annual_salary = models.BigIntegerField(default=50000)
    bank_balance = models.BigIntegerField(default=50000)
    debt = models.BigIntegerField(default=0)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    
    # groups = models.ManyToManyField(Group, related_name='custom_user_set')
    # user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')
    def __str__(self):
        return f"{self.email}"