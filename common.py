import datetime
import os
import pathlib
from datetime import timezone
from pathlib import Path


def get_path():
    path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
    return path

def remove_file(path_to_file):
    pathlib.Path.unlink(Path(path_to_file))

def get_utc_timestamp():
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = str(utc_time.timestamp()).replace('.', '')
    return utc_timestamp


def get_current_timestamp():
    timestamp = datetime.datetime.now()
    return timestamp.strftime("%Y%m%d-%H:%M:%S.%f")[:-3]


def list_files(path):
    list_of_files = []
    for root, dirs, files in os.walk(Path(path)):
        for file in files:
            list_of_files.append(os.path.join(root,file))
    return list_of_files


def get_delivery_params(param_string):
    transport = None
    host = None
    login = None
    password = None
    key = None
    folder = None
    port = None
    local = None
    id = None
    remote_file = None
    spool_file = None
    file = None
    if isinstance(param_string, list):
        param_string = param_string[0]
    transport = param_string.get('transport')
    host = param_string.get('host')
    login = param_string.get('login')
    folder = param_string.get('folder')
    port = param_string.get('port')
    local = param_string.get('local')
    password = param_string.get('password')
    key = param_string.get('ftp_identity')
    id = param_string.get('id')
    remote_file = param_string.get('remote_file')
    spool_file = param_string.get('spool_file')
    file = param_string.get('file')
    spool = param_string.get('spool')
    return {'transport': transport, 'host': host, 'login': login,
            'password': password, 'key': key, 'folder': folder, 'port': port,
            'local': local, 'id': id, 'remote_file': remote_file, 
            'spool_file': spool_file, 'file': file, 'spool': spool}


def write_log(log_file, message_type, params, error=None):
    message = None
    login=params.get('login')
    password=params.get('password')
    host=params.get('host')
    port=params.get('port')
    remote_file=params.get('remote_file')
    spool_file=params.get('spool_file')
    with open(log_file, 'a+') as log:
        if message_type == 'connecting':
            message = f"\nDEB [{get_current_timestamp()}] Going to connect to {login}:{password}@{host}:{port}"
        if message_type == 'connect_failed':
            message = f"\nDEB [{get_current_timestamp()}] FAILED to connect to {login}:{password}@{host}:{port}. {error}"
        if message_type == 'uploading':
            message = f"\nDEB [{get_current_timestamp()}] Going to upload {spool_file} to {login}:{password}@{host}:{port} {remote_file}"
        if message_type == 'uploaded': 
            message = f"\nDEB [{get_current_timestamp()}] File {spool_file} UPLOADED to {login}:{password}@{host}:{port} {remote_file}"
        if message_type == 'failed': 
            message = f"\nDEB [{get_current_timestamp()}] FAILED {spool_file} upload to  {login}:{password}@{host}:{port} {remote_file}. {error}"
        log.write(message)