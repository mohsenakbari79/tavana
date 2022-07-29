from celery import shared_task 
# from config.celery import app
from time import sleep
@shared_task(name="enable")
def my_tassk():
    with open("test.txt",'w',encoding = 'utf-8') as f:
        for x in range(10):
            f.write(str(x))
            print(x)
            sleep(1)
        