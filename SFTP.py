import pysftp
import pathlib
import logging

from requests import exceptions
from sqlalchemy import and_, or_, not_

from db import db_session
from models import Job
from common import get_utc_timestamp, get_delivery_params, get_path, remove_file, write_log, list_files

PATH = get_path()

logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def put_files(delivery, sftp):
    status = []
    for task in delivery:
        params = get_delivery_params(task)
        # convert dict entries to vars
        log_file = str(PATH / 'connection_logs' / str(id))
        write_log(log_file, 'uploading', params)
        try:
            sftp.put(str(params['spool_file']), params['remote_file'])
            params.update(status='Completed', last_status_ts=get_utc_timestamp())
            status.append(params)
            write_log(log_file, 'uploaded', params)
        except Exception as error:
            params.update(status='Error', last_status_ts=get_utc_timestamp(), last_error=str(error))
            status.append(params)
            write_log(log_file, 'failed', params, str(error))
            continue 
    return status


def SFTP_upload(delivery):
    status = []
    params = get_delivery_params(delivery)
    log_file = str(PATH / 'connection_logs' / str(id))
    cnopts = pysftp.CnOpts()
    cnopts.compression = True
    cnopts.log = log_file
    write_log(log_file, 'connecting', params)
    if not params['key']:
        try:
            with pysftp.Connection(
                host=params['host'],
                username=params['login'],
                password=params['password'],
                port=params['port'],
                cnopts=cnopts
            ) as sftp:
                sftp.pwd   # need this to cathc exception if not connected
                status=put_files(delivery, sftp)
        except Exception as error:
                job=Job.query.filter(Job.id == params['id']).\
                update({
                    'status': 'Error',
                    'last_error': str(error),
                    'last_status_ts':get_utc_timestamp(),
                    'attempts': (Job.attempts + 1)
                })
                db_session.commit()
                write_log(log_file, 'connect_failed', params)
                raise Exception
    else:
        with pysftp.Connection(
            host=params['host'],
            username=params['login'],
            password=params['password'],
            port=params['port'],
            private_key=params['key'],
            cnopts=cnopts
        #    private_key='./Users/apetrov/Documents/mykey_Canada/id_rsa'
        ) as sftp:
            status = put_files(delivery, sftp)
    for i in status:
        job = Job.query.filter(and_(Job.id == i['id'], Job.file == i['file'])).\
            update({
                'status': i.get('status'),
                'last_error': i.get('last_error'),
                'last_status_ts': i.get('last_status_ts'),
                'attempts': (Job.attempts + 1),
                })
        db_session.commit()
        ## remove uploaded files
        if i.get('status')=='Completed':
            remove_file(i.get('spool_file'))
    ## check if there are any files except message

    try:
        pathlib.Path(params['folder']).rmdir()
    except:
        pass ## Pass if dir is not empty