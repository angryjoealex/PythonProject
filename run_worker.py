import requests
from dramatiq.brokers.redis import RedisBroker 
import dramatiq

from get_job import get_task

dramatiq.set_broker(RedisBroker())

@dramatiq.actor(max_retries=3, min_backoff=120000)
def send_files(id):
    get_task(id)
