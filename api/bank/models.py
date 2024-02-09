from django.db import models
from .choices import DurationType, IntervalType

class Bank(models.Model):
    balance = models.DecimalField(max_digits=20,decimal_places=2)
    updated = models.DateTimeField(auto_now=True)

    def is_available(self,amount):
        return amount<=self.balance

class Loan(models.Model):
    min_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2)
    duration = models.IntegerField(choices=DurationType)
    interval = models.IntegerField(choices=IntervalType)
    interest_rate = models.DecimalField(max_digits=5,decimal_places=2)
