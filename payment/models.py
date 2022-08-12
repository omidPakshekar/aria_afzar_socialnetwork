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

MONTH_CHOICE = (
    ('1 Month', '1'),
    ('3 Month', '3'),
    ('6 Month', '6'),
    ('12 Month', '12'),
    
)


class Payment(models.Model):
    user            = models.ForeignKey(CustomeUserModel, related_name='payments', null=True, on_delete=models.SET_NULL)
    created_date    = models.DateTimeField(verbose_name='date create', auto_now_add=True)
    created_time    = models.TimeField(blank=False,  auto_now_add=True)
    amount          = models.DecimalField(blank=False, decimal_places=2, max_digits=10)
    payment_system  = models.CharField(max_length=20, choices=PAYMENT_MESSAGE)
    status          = models.CharField(max_length=20, choices=STATUS_MESSAGE)

    def __str__(self) -> str:
        return f"{self.user.wallet} / amount= {self.amount} / {self.created_date}" 

class PiggyBank(models.Model):
    amount          = models.DecimalField(blank=False, decimal_places=2, max_digits=10)
    started_time    = models.DateTimeField(verbose_name='date create', auto_now_add=True)
    expired_day     = models.IntegerField(default=0)
     

class MemberShip(models.Model):
    user    = models.OneToOneField(CustomeUserModel, related_name='membership',  on_delete=models.CASCADE)
    month   =  models.CharField(max_length=20, choices=MONTH_CHOICE)
    amount  = models.DecimalField(blank=True, decimal_places=2, max_digits=10)
    started_date =  models.DateTimeField(verbose_name='date_create', auto_now_add=True)  
    expired_day = models.IntegerField(default=0)

"""
    signal -- create expire day and amount automaticly  
"""
@receiver(pre_save, sender=MemberShip)
def blog_post_pre_save(sender, instance, *args, **kwargs):
    if instance.amount == None:
        if instance.month == '1':
            instance.amount = 24.87
            instance.expired_day = 30
        elif instance.month == '3':
            instance.amount = 64.47
            instance.expired_day = 90
        elif instance.month == '6':
            instance.amount = 117.47
            instance.expired_day = 180
        else:
            instance.amount = 238.87
            instance.expired_day = 360
        instance.save()




