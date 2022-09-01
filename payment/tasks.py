from __future__ import absolute_import, unicode_literals
import time
from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone

from celery import shared_task
from celery.utils.log import get_task_logger
from core.celery import app

from .models import PiggyBank, TransactionHistory
from users.models import *

logger = get_task_logger(__name__)

def add_money_wallet(user_add_money, user_cost_money, amount):
    w =  user_add_money.wallet
    w.amount += Decimal(amount)
    w.save()
    TransactionHistory(kind='piggy', amount=amount, owner=user_add_money)
    TransactionHistory(kind='piggy', amount=-1*amount, owner=user_cost_money)

@app.task
def check_piggy():
    """
        activity number = 0  ---> piggy money transfer to admin
        activity number <= 5 ---> 50% admin, 50% to user
        activity number > 5  ---> all of money to user
    """
    piggy_ = PiggyBank.objects.filter(finish_time__lte=timezone.now())
    admin = CustomeUserModel.objects.get(id=1)
    for piggy in piggy_:
        piggy_activity = piggy.activity.all()
        number =  piggy_activity.aggregate(Sum('number'))['number__sum']
        if number == 0:
            add_money_wallet(user_add_money=admin, user_cost_money=piggy.user, amount=piggy.amount)
        else:
            pigg_amount = piggy.amount
            if number <= 5:
                pigg_amount /= 2
                add_money_wallet(user_add_money=admin, user_cost_money=piggy.user, amount=pigg_amount)
            money_unit = Decimal(pigg_amount / number)
            for activity in piggy_activity:
                add_money_wallet(user_add_money=activity.user, user_cost_money=piggy.user, amount = money_unit * activity.number)
                activity.delete()
        piggy.delete()
