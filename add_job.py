from db import db_session

from models import Job
from run_worker import send_files
# from run_worker import print_error,print_result

DEFAULT_PORTS = {
   'SFTP': 22,
   'FTP': 21
}


def add_task(delivery):
    for task in delivery:
        if not task['port']:
            task['port'] = DEFAULT_PORTS.get(task['transport'])
        if not task['local']:
            task['local'] = 0
        options = str(task['options'])[:999]
        add_job = Job(
            id=task['id'],
            added=task['added'],
            postfix_id=task['postfix_id'],
            transport=task['transport'],
            host=task['host'],
            login=task['login'],
            password=task['password'],
            port=task['port'],
            folder=task['folder'],
            key=task['key'],
            file=task['file'],
            filetitle=task['filetitle'],
            spool=task['spool'],
            local=int(task['local']),
            status=task['status'],
            options=options,
            new_filename=task['new_filename'],
            failyre_reply=task['failyre_reply'],
            succes_reply=task['succes_reply'],
            attempts=0
            )
        db_session.add(add_job)
        db_session.commit()
    send_files.send(delivery[0]['id'])