from __future__ import absolute_import, unicode_literals
import time
from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone

from celery import shared_task
from celery.utils.log import get_task_logger
from core.celery import app

from .models import PiggyBank
from users.models import *

logger = get_task_logger(__name__)

def add_money_wallet(id, amount):
    w = Wallet.objects.get(id=id)
    w.amount += Decimal(amount)
    w.save()

@app.task
def check_piggy():
    """
        activity number = 0  ---> piggy money transfer to admin
        activity number <= 5 ---> 50% admin, 50% to user
        activity number > 5  ---> all of money to user
    """
    piggy_ = PiggyBank.objects.filter(finish_time__lte=timezone.now())
    for piggy in piggy_:
        piggy_activity = piggy.activity.all()
        number =  piggy_activity.aggregate(Sum('number'))['number__sum']
        if number == 0:
            add_money_wallet(1, piggy.amount)
        else:
            pigg_amount = piggy.amount
            if number <= 5:
                pigg_amount /= 2
                add_money_wallet(1, pigg_amount)
            money_unit = Decimal(pigg_amount / number)
            for activity in piggy_activity:
                add_money_wallet(activity.user.id, money_unit * activity.number)
                activity.delete()
        piggy.delete()
    activity = Activity.objects.filter(piggy=piggy_)

