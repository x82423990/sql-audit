# coding=utf-8
from celery import shared_task
from .models import Inceptsql
import time


@shared_task()
def change_oder_status(sql_oder_id):
    instance = Inceptsql.objects.get(pk=sql_oder_id)
    time.sleep(60)
    instance.status = 3
    instance.save()
