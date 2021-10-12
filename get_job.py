from SFTP import SFTP_upload
from models import Job
from common import get_path

PATH = get_path()
# job_id_test = 1634028543835628


def get_task(id):
    delivery = []
    job_to_do = Job.query.filter(Job.id == id)

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
            'key': str(PATH/file.key) if file.key else file.key,
            'file': file.file,
            'spool_file':f"{file.spool}/{file.file}",
            'spool': file.spool,
            'local': file.local
        })
    if delivery[0]['transport'] == 'SFTP':
        SFTP_upload(delivery)

# get_task(job_id_test)
