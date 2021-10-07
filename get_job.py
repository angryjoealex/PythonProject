import pathlib
import os

import SFTP
from models import Job

PATH = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
job_id_test = 1633544566870036


def get_job(job_id):
    delivery = []
    job_to_do = Job.query.filter(Job.id == job_id)

    for file in job_to_do:
        delivery.append({
            'id': file.id,
            'transport': file.transport,
            'host': file.host,
            'login': file.login,
            'password': file.password,
            'port': file.port,
            'remote_dir': file.remote_dir,
            'remote_file': f"{file.remote_dir}/{file.file}",
            'key': str(PATH/file.key),
            'file': file.file,
            'spool_file':f"{file.spool}/{file.file}",
            'spool': file.spool,
            'local': file.local
        })
    if delivery[0]['transport'] == 'SFTP':
        SFTP.SFTP_upload(delivery)


get_job(job_id_test)
