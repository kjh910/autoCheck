from django.shortcuts import redirect, reverse
import requests
from django.conf import settings
import datetime

def task_send_email_every_hour():
    response = requests.get(
            settings.SEARCH_LINK
    )
    print(
            {
                'Response':response,
                'Time':datetime.datetime.now()
           }
            )