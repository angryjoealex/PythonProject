import pysftp
import pathlib
import os

from db import db_session
from models import Job
from common import get_utc_timestamp
from common import get_path

PATH = get_path()

def put_files(delivery, sftp):
    for file in delivery:
        remote_file = file['remote_file']
        local_file = file['spool_file']
        try:
            sftp.put(local_file, remote_file)
            job = Job.query.filter(Job.id == file['id'] and Job.file == file['file']).\
            update({
                'status': 'Completed',
                'last_error': '',
                'last_status_ts': get_utc_timestamp()
                })
            db_session.commit()
        except Exception as error:
            job = Job.query.filter(Job.id == file['id'] and Job.file == file['file']).\
            update({'status': 'Error', 'last_error': f"{error}", 'last_status_ts': get_utc_timestamp()})
            db_session.commit()
            return Exception



def SFTP_upload(delivery):
    if not delivery[0]['key']:
        try:
            with pysftp.Connection(
                host=delivery[0]['host'],
                username=delivery[0]['login'],
                password=delivery[0]['password'],
                port=delivery[0]['port'],
                log=str(PATH / 'connection_logs' / str(delivery[0]['id']))
            ) as sftp:
                put_files(delivery, sftp)
        except Exception as error:
                job = Job.query.filter(Job.id == delivery[0]['id']).\
                update({
                    'status': 'Error',
                    'last_error': f"Can't connect to {delivery[0]['host']}:{delivery[0]['port']} \n {error}",
                    'last_status_ts':get_utc_timestamp() 
                })
                db_session.commit()
                return Exception
    else:
        with pysftp.Connection(
            host=delivery[0]['host'],
            username=delivery[0]['login'],
            password=delivery[0]['password'],
            port=delivery[0]['port'],
            private_key=delivery[0]['key']
        #    private_key='./Users/apetrov/Documents/mykey_Canada/id_rsa'
        ) as sftp:
            put_files(delivery, sftp)