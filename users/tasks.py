from __future__ import absolute_import, unicode_literals
import time
from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone

from celery import shared_task
from celery.utils.log import get_task_logger
from core.celery import app

from users.models import MemberShip

logger = get_task_logger(__name__)


@app.task
def check_membership():
    memberShip = MemberShip.objects.filter(finish_date__lte=timezone.now())
    for member in memberShip:
        user = member.user
        user.have_membership = False
        user.save()
        member.delete()