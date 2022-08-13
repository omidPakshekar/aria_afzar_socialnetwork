from datetime import datetime
from django.db import models
from django.db.models.signals import (pre_save, post_save)
from django.dispatch import receiver

from users.models import CustomeUserModel

STATUS_MESSAGE = (
    ('Accept', 'Accept'),
    ('Reject', 'Reject'),
    ('Pending', 'Pending'),
)

PAYMENT_MESSAGE = (
    ('Bitcoin', 'Bitcoin'),
    ('Visa', 'Visa'),
    ('Ether', 'Ether'),
)


class Payment(models.Model):
    user            = models.ForeignKey(CustomeUserModel, related_name='payments', null=True, on_delete=models.SET_NULL)
    created_date    = models.DateTimeField(verbose_name='date create', auto_now_add=True)
    created_time    = models.TimeField(blank=False,  auto_now_add=True)
    amount          = models.DecimalField(blank=False, decimal_places=2, max_digits=10)
    payment_system  = models.CharField(max_length=20, default='Pending' ,choices=PAYMENT_MESSAGE)
    status          = models.CharField(max_length=20, choices=STATUS_MESSAGE)

    def __str__(self) -> str:
        return f"{self.user.wallet} / amount= {self.amount} / {self.created_date}" 

class PiggyBank(models.Model):
    amount          = models.DecimalField(blank=False, decimal_places=2, max_digits=10)
    started_time    = models.DateTimeField(verbose_name='date create', auto_now_add=True)
    expired_day     = models.IntegerField(default=0)
     




