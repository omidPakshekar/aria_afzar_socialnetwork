from __future__ import absolute_import, unicode_literals
import time

from celery import shared_task
from celery.utils.log import get_task_logger
from core.celery import app

from django.utils import timezone
from .models import PiggyBank
from users.models import Activity, CustomeUserModel


@app.task
def my_task():
    time.sleep(10)
    f = open("demofile3.txt", "w")
    f.write("Woops! I have deleted the content!")
    f.close()

@app.task
def check_piggy():
    piggy_ = PiggyBank.objects.filter(finish_time__lte=timezone.now())
    activity = Activity.objects.filter(piggy=piggy_)
    print('piggy_', piggy_)

