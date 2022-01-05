
import requests
import datetime
import os

def task_send_email_every_hour():
    response = requests.get(
            os.getenv('SEARCH_LINK','http://127.0.0.1/search')
    )
    print(
            {
                'Response':response.json(),
                'Time':datetime.datetime.now()
           }
            )
task_send_email_every_hour()