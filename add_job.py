from db import db_session
from models import Job

DEFAULT_PORTS = {
   'SFTP':22,
   'FTP':21
}

def insert(data):
    for task in data:
        if not task['port']:
            task['port'] = DEFAULT_PORTS.get(task['transport'])
        if not task['local']:
            task['local'] = 0
        add_job = Job(
            id=task['id'],
            postfix_id=task['postfix_id'],
            transport=task['transport'],
            host=task['host'],
            login=task['login'],
            password=task['password'],
            port=task['port'],
            remote_dir=task['remote_dir'],
            key=task['key'],
            file=task['file'],
            spool=task['spool'],
            local=task['local'],
            status=task['status'],
            attempts=1
            )
        db_session.add(add_job)
        db_session.commit()
