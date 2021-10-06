import SFTP
from models import Job

job_id_test = 1633524397712855


def get_job(job_id):
    delivery=[]
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
            'key': file.key,
            'file': file.file,
            'spool_file':f"{file.spool}/{file.file}",
            'spool': file.spool,
            'local': file.local
        })
    if delivery[0]['transport'] == 'SFTP':
        SFTP.SFTP_upload(delivery)


get_job(job_id_test)
