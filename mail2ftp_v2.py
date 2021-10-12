import logging
import pathlib
import re
import sys
from ast import literal_eval

import mailparser

from common import get_utc_timestamp
from common import get_path
from add_job import add_task

PATH = get_path()
SPOOL_PATH = PATH / 'spool'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.ERROR,
                    filename=PATH / 'mail2_ftp2.log')


def remove_file(path_to_file):
    pathlib.Path.unlink(path_to_file)


def get_delivery_params(param_string):
    transport = None
    host = None
    login = None
    password = None
    key = None
    remote_dir = None
    port = None
    local = None
    transport = param_string.get('transport')
    host = param_string.get('host')
    login = param_string.get('login')
    remote_dir = param_string.get('folder')
    port = param_string.get('port')
    local = param_string.get('local')
    password = param_string.get('password')
    key = param_string.get('ftp_identity')
    if not (transport and host and remote_dir and (password or key)):
        print(f"Delivery params are not fully defined transport: {transport}, host: {host}, password: {password},remote_dir: {remote_dir} identity: {key}")
        exit(0)
    return transport, host, login, password, key, remote_dir, port, local


def save_mail_body(path, mail):
    try:
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        # save email body
        with open(path / 'message', 'w+') as message_body:
            message_body.write(mail)
    except PermissionError as error:
        print(f"Can't write email body.\n {error}")
        exit(0)


def save_attached(mail, utc_ts, spool_path_file, upload_creds, received_id_posfix):
    """This function get files from attach and save it to spool"""
    payload = []
    transport, host, login, password, key, remote_dir, port, local = get_delivery_params(upload_creds)
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
            mail.write_attachments(SPOOL_PATH/utc_ts)
        except PermissionError as error:
            print(f"{error}.\n Can't write attached file")
            return
        payload.append({
            'id': utc_ts,
            'postfix_id': received_id_posfix,
            'transport': transport,
            'host': host,
            'login': login,
            'password': password,
            'port': port,
            'remote_dir': remote_dir,
            'key': key,
            'file': filename,
            'spool': str(spool_path_file),
            'local': local,
            'status': 'initial delivery'
        })
    return payload


def main():
    delivery = []
    utc_ts = get_utc_timestamp()
    raw_email = SPOOL_PATH / utc_ts

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

    # create spool folder for POSTFIX mail ID
    spool_path_file = SPOOL_PATH / utc_ts
    save_mail_body(spool_path_file, mail.body)

    # search params for delivery in mail body
    get_param = re.search('mail2ftp:\{.+\}', mail.body)
    try:
        get_param.group(0)
    except AttributeError:
        print('No deilvery parameters are defined')
        return
    upload_creds = get_param.group(0).replace('mail2ftp:', '')
    upload_creds = re.sub(r"(\w+): ", r"'\1':", upload_creds).replace(' ', '')
    upload_creds = literal_eval(upload_creds)
    # Save attached files and populate delivery parameters for database insert
    delivery = save_attached(mail, utc_ts, spool_path_file, upload_creds, received_id_posfix)

    # add job to database
    add_task(delivery)


if __name__ == "__main__":
    main()
