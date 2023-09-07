from django.db import models
from user_app.models import User

# Create your models here.
class Transaction(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transaction")
    amount = models.BigIntegerField()
