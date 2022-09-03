from datetime import datetime
from django.db import models
from django.db.models.signals import (pre_save, post_save)
from django.dispatch import receiver
from django.utils import timezone

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

KIND_CHOICES = (
    ('withdraw', 'withdraw'),
    ('deposit', 'deposit'),
    ('listen', 'listen'),
    ('like', 'like'),
    ('membership', 'membership'),
    ('piggy', 'piggy'),
    ('donate', 'donate')
)


class Payment(models.Model):
    user            = models.ForeignKey(CustomeUserModel, related_name='payments', null=True, on_delete=models.SET_NULL)
    created_date    = models.DateTimeField(verbose_name='date create', auto_now_add=True)
    created_time    = models.TimeField(blank=False,  auto_now_add=True)
    amount          = models.DecimalField(blank=False, decimal_places=4, max_digits=12)
    payment_system  = models.CharField(max_length=20, choices=PAYMENT_MESSAGE)
    status          = models.CharField(max_length=20, default='Pending', choices=STATUS_MESSAGE)
    description     = models.TextField(blank=True)
    done            = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.username} / amount= {self.amount} / {self.created_date}" 

class PiggyBank(models.Model):
    user            = models.ForeignKey(CustomeUserModel, related_name='user_piggy', on_delete=models.CASCADE)
    amount          = models.DecimalField(blank=False, decimal_places=4, max_digits=12)
    started_time    = models.DateTimeField()
    finish_time     = models.DateTimeField()
    expired_day     = models.IntegerField(default=0)
    current         = models.BooleanField(default=False)
    long            = models.BooleanField(default=False)
    class Meta:
        ordering  = ['started_time']
    @property
    def day_left(self):
        return self.finish_time - timezone.now()


class TransactionHistory(models.Model):
    owner        = models.ForeignKey(CustomeUserModel, related_name='transaction', on_delete=models.CASCADE)
    amount       = models.DecimalField(decimal_places=4, max_digits=12)
    created_time = models.DateTimeField(blank=False,  auto_now_add=True)
    kind         = models.CharField(max_length=20, choices=KIND_CHOICES)

    
