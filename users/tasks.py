from selery import shared_task
from time import sleep

@shared_task
def sleepy(duration):
	sleep(duration)
	return None