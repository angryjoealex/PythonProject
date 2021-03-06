import logging
import pathlib
import re
import sys
import shutil
import uuid
from ast import literal_eval


import mailparser

from common import get_utc_timestamp, get_path, get_delivery_params, remove_file, get_date
from add_job import add_task

PATH = get_path()
SPOOL_PATH = PATH / 'spool'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,
                    filename=PATH / 'mail2_ftp2.log',
                    filemode='a'
                    )
logger = logging.getLogger(__name__)

def save_mail_body(path, mail):
    try:
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        # save email body
        with open(path / 'message', 'w+') as message_body:
            message_body.write(mail)
    except PermissionError as error:
        print(f"Can't write email body.\n {error}")
        exit(0)


def save_attached(mail, task_uuid, utc_ts, spool_path_file, params, received_id_posfix):
    """This function get files from attach and save it to spool"""
    payload = []
    files =[]
    if not params.get('local'):
        for attach in mail.attachments:
            filename = re.search('filename=".*"', attach['content-disposition'].replace('\n', ' '))
            try:
                filename.group(0)
                filename = filename.group(0).replace('filename=', '').replace('"', '')
            except IndexError:
                print("Can't get attach name")
                return
            # write attach to spool and polpulate delivery variable
            try:
                mail.write_attachments(spool_path_file)
            except PermissionError as error:
                print(f"{error}.\n Can't write attached file")
                return
            files.append(filename)
    else: #if it is local delivery - get files from options mail2ftp:{...options:{'local_files':[{'filename':'filename1', 'filetitle':'filename1'},..]}}
        files = params.get('options').get('local_files')
    for filename in files:
        filetitle = None
        file = filename
        if params.get('local'):
            file = filename.get('filename')
            filetitle = filename.get('filetitle')
        payload.append({
                'id':task_uuid,
                'added': utc_ts,
                'postfix_id': received_id_posfix,
                'transport': params.get('transport'),
                'host': params.get('host'),
                'login': params.get('login'),
                'password': params.get('password'),
                'port': params.get('port'),
                'folder': params.get('folder'),
                'key': params.get('key'),
                'file': file ,
                'filetitle': filetitle,
                'spool': str(spool_path_file),
                'local': params.get('local'),
                'status': 'initial delivery',
                'options': params.get('options'),
                'new_filename': params.get('new_filename'),
                'failyre_reply': params.get('failyre_reply'),
                'succes_reply': params.get('succes_reply')
            })
    return payload


def main():
    delivery = []
    utc_ts = get_utc_timestamp()
    task_uuid = str(uuid.uuid4())
    task_date = str(get_date())
    raw_email = SPOOL_PATH / task_uuid

    # Read mail from POSTFIX
    data = sys.stdin.read()
    try:
        with open(raw_email, 'w+') as file:
            file.write(data)
    except (FileNotFoundError, PermissionError) as error:
        print(f"{error}\nCan't write raw email")
        return
    # Parse email from file  and delete raw email
    mail = mailparser.parse_from_file(raw_email)
    remove_file(raw_email)
    # Get POSTFIX mail ID
    for received in mail.received:
        if 'with' in received:
            received_id_posfix = received['id']

    # create spool folder
    spool_path_file = SPOOL_PATH / task_date / task_uuid
    save_mail_body(spool_path_file, mail.body)

    # search params for delivery in mail body
    get_param = re.search('mail2ftp:\{.+\}', mail.body)
    try:
        get_param.group(0)
    except AttributeError:
        print('No deilvery parameters are defined')
        return
    upload_creds = get_param.group(0).replace('mail2ftp:', '')
    upload_creds = re.sub(r"(\w+): ", r"'\1':", upload_creds)
    upload_creds = literal_eval(upload_creds)  #sting to dict
    params = get_delivery_params(upload_creds)
    if not (params['transport'] and params['host'] and params['folder'] and (params['password'] or params['key'])):
        print(f"Delivery params are not fully defined transport: {params['transport']}.\
            , host: {params['host']}, password: {params['password']}.\
            ,remote_dir:{params['folder']}, identity: {params['key']}")
        shutil.rmtree(spool_path_file, ignore_errors=True) #delete saved
        exit(0)
    # Save attachedfiles or just set local files and populate delivery parameters for database insert
    delivery = save_attached(mail, task_uuid, utc_ts, spool_path_file, params, received_id_posfix)

    # add job to database
    add_task(delivery)


if __name__ == "__main__":
    main()
