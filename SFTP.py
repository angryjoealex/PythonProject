import pysftp


def put_files(job,sftp):
    for file in job:
                    remote_file = file['remote_file']
                    local_file = file['spool_file']
                    sftp.put(local_file, remote_file)


def SFTP_upload(delivery):
    if not delivery[0]['key']:
        with pysftp.Connection(
            host=delivery[0]['host'],
            username=delivery[0]['login'],
            password=delivery[0]['password'],
            port=delivery[0]['port']
        ) as sftp:
            put_files(delivery, sftp)
    else:
        with pysftp.Connection(
            host=delivery[0]['host'],
            username=delivery[0]['login'],
            password=delivery[0]['password'],
            port=delivery[0]['port'],
            private_key=delivery[0]['key']
        ) as sftp:
            put_files(delivery, sftp)