from models import job

job_to_do = job.query.filter(job.id==1633515776793665)
# print(job_to_do)
#print(f'id: {job.id}, file: {job.file}, transport: {job.transport}')
for task in job_to_do:
    print(f'id: {task.id}, file: {task.file}, transport: {task.transport}')