import shutil

import dramatiq
import requests


from dramatiq.brokers.rabbitmq import RabbitmqBroker
from sqlalchemy import and_, or_, not_, func
from sqlalchemy.sql import text

from db import db_session
from get_job import get_task
from models import Job

from db import engine
from common import send_mail


EXCEEDED = 'All delivery retries failed'
EXCEEDED_QUERY ="SELECT CONCAT('Hello. Exceded upload attempts for files: ', string_agg(CONCAT(folder,file),', '), 'configured to delivery to ', host  ) as msg, failyre_reply\
 FROM mail2ftp WHERE id = :id\
 GROUP BY id, host, failyre_reply"

dramatiq.set_broker(RabbitmqBroker(url="amqp://guest:guest@127.0.0.1:5672"))

@dramatiq.actor(max_retries=0, min_backoff=120000)
def send_files(id):
    get_task(id)

@dramatiq.actor
def get_delay(message, delay, exceeded):
    if isinstance(message, dict) and message.get('actor_name') == 'send_files':
        job_id = message.get('args')[0]
        job = Job.query.filter(and_(Job.id == job_id, Job.status != 'Completed'))
        if not exceeded:
            job.update({'next_attempt': (Job.last_status_ts + func.coalesce(delay*1000, 0))})
            db_session.commit()
        else:
            job.update({'status': EXCEEDED, 'next_attempt': None})
            db_session.commit()
            del_spool = Job.query.filter(and_(Job.id == job_id, Job.status == EXCEEDED)).first()
            shutil.rmtree(del_spool.spool, ignore_errors=True)
            fail_message = engine.execute(text(EXCEEDED_QUERY), id =job_id )
            for msg in fail_message:
                send_mail(msg[1], 'Delivery failure', msg[0])
