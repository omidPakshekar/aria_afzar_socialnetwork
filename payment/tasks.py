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

@app.task
def my_task():
    time.sleep(10)
    f = open("demofile3.txt", "w")
    f.write("Woops! I have deleted the content!")
    f.close()

@app.task
def check_piggy():
    piggy_ = PiggyBank.objects.filter(finish_time__lte=timezone.now())
    for piggy in piggy_:
        piggy_activity = piggy.activity.all()
        number =  piggy_activity.aggregate(Sum('number'))['number__sum']
        money_unit = Decimal(piggy.amount / number)
        for activity in piggy_activity:
            w = Wallet.objects.get(id=activity.user.id)
            w.amount += Decimal(money_unit * activity.number)
            w.save()
            activity.delete()
        piggy.delete()
    activity = Activity.objects.filter(piggy=piggy_)

