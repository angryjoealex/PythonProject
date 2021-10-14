from SFTP import SFTP_upload
from models import Job
from common import get_path

from sqlalchemy import and_, or_, not_

PATH = get_path()


def get_task(id):
    delivery = []
    job_to_do = Job.query.filter(and_(Job.id == id, Job.status != 'Completed'))

    for file in job_to_do:
        delivery.append({
            'id': file.id,
            'transport': file.transport,
            'host': file.host,
            'login': file.login,
            'password': file.password,
            'port': file.port,
            'folder': file.folder,
            'remote_file': f"{file.folder}/{file.file}",
            'key': file.key,
            'file': file.file,
            'spool_file':f"{file.spool}/{file.file}",
            'spool': file.spool,
            'local': file.local
        })
    if delivery[0]['transport'] == 'SFTP':
        SFTP_upload(delivery)
