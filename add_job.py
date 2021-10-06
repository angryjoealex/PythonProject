import sys
from db import db_session
from models import job


def insert(data):
    for task in data:
        if not task['port']:
            if task['transport'] == 'SFTP':
                task['port'] = '22'
            elif task['transport'] == 'FTP':
                task['port'] = '21'
        if not task['local']:
            task['local'] = 0
        add_job = job(
            id=task['id'],
            postfix_id=task['postfix_id'],
            transport=task['transport'],
            host=task['host'],
            login=task['login'],
            password=task['password'],
            port=task['port'],
            remote_dir=task['remote_dir'],
            key=task['identity'],
            file=task['file'],
            local=task['local'],
            attempts=1
            )
        db_session.add(add_job)
        db_session.commit()

if __name__ == '__main__':
    insert(data)