import shutil

import dramatiq
import requests


from dramatiq.brokers.rabbitmq import RabbitmqBroker
from sqlalchemy import and_, or_, not_, func

from db import db_session
from get_job import get_task
from models import Job

dramatiq.set_broker(RabbitmqBroker(url="amqp://guest:guest@127.0.0.1:5672"))

@dramatiq.actor(max_retries=2, min_backoff=120000)
def send_files(id):
    get_task(id)

# @dramatiq.actor
# def print_result(message_data, result):
#     print(f"The result of message {message_data['message_id']} was {result}.")
#     print(str(result))

# @dramatiq.actor
# def print_error(message_data, exception_data):
#     print(f"Message {message_data['message_id']} failed:")
#     print(f"  * type: {exception_data['type']}")
#     print(f"  * message: {exception_data['message']!r}")
#     print(str(message_data))

@dramatiq.actor
def get_delay(message, delay, exceeded):
    if isinstance(message, dict):
            if message.get('actor_name') == 'send_files':
                job_id=message.get('args')[0]
                if not exceeded:
                    job=Job.query.filter(and_(Job.id == job_id, Job.status != 'Completed')).\
                        update({'next_attempt': (Job.last_status_ts + func.coalesce(delay*1000,0))})
                    db_session.commit()
                else:
                    job=Job.query.filter(and_(Job.id == job_id, Job.status != 'Completed')).\
                        update({'status': 'All delivery retries failed', 'next_attempt':None})
                    db_session.commit()
                    del_spool=Job.query.filter(and_(Job.id == job_id, Job.status == 'All delivery retries failed')).first()
                    shutil.rmtree(del_spool.spool, ignore_errors=True)