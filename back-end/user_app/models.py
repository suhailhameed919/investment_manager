from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField()
    annual_salary = models.BigIntegerField()
    bank_balance = models.BigIntegerField()
    debt = models.BigIntegerField()

    def __str__(self):
        return f"{self.email}"