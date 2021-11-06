import shutil

from sqlalchemy import and_, or_, not_

from db import db_session
from common import get_path, remove_file, list_files
from models import Job
# from transport import Transport
from transport_new import Transport

PATH = get_path()


def get_task(id):
    delivery = []
    error = None
    job_to_do = Job.query.filter(and_(Job.id == id, Job.status != 'Completed'))

    for file in job_to_do:
        spool_file = f"{file.spool}/{file.file}"
        remote_file = f"{file.folder}/{file.file}"
        if file.local:
            spool_file = file.file
            remote_file = f"{file.folder}/{file.filetitle}"
        delivery.append({
            'id': file.id,
            'transport': file.transport,
            'host': file.host,
            'login': file.login,
            'password': file.password,
            'port': file.port,
            'folder': file.folder,
            'remote_file': remote_file,
            'key': file.key,
            'file': file.file,
            'spool_file': spool_file,
            'spool': file.spool,
            'local': file.local
        })
    connection = Transport(delivery)
    status = connection.put()
    for i in status:
        job = Job.query.filter(and_(Job.id == i['id'], Job.file == i['file'])).\
            update({
                'status': i.get('status'),
                'last_error': i.get('last_error'),
                'last_status_ts': i.get('last_status_ts'),
                'attempts': (Job.attempts + 1),
                'next_attempt': i.get('next_attempt'),
                })
        db_session.commit()
        if i.get('last_error'):
            error = i.get('last_error')
        # remove uploaded files if not local delivery
        if i.get('status') == 'Completed' and not i.get('local'):
            remove_file(i.get('spool_file'))
    # check if there are any files except message
    if error:
        raise Exception('Restart task')
    # check if there any attachments    
    files = list_files(delivery[0]['spool'])
    files.remove('message')
    if len(files) == 0:
        shutil.rmtree(delivery[0]['spool'], ignore_errors=True)
