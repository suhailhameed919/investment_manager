from django.db import models
from user_app.models import User
from category_app.models import Category

# Create your models here.
class Transaction(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transaction")
    amount = models.BigIntegerField()
    category = models.ManyToManyField(Category, related_name="transaction")