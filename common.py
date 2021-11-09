import datetime
import os
import pathlib
import sys
import smtplib

from datetime import timezone
from pathlib import Path

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

def get_path():
    path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
    return path


def remove_file(path_to_file):
    pathlib.Path.unlink(Path(path_to_file))


def get_utc_timestamp():
    utc_timestamp = str(datetime.datetime.utcnow().strftime("%s.%f")).replace('.', '')
    return utc_timestamp


def get_current_timestamp():
    timestamp = datetime.datetime.now()
    return timestamp.strftime("%Y%m%d-%H:%M:%S.%f")[:-3]

def get_date():
    timestamp = datetime.datetime.now()
    return timestamp.strftime("%m%d%Y")

def list_files(path):
    list_of_files = []
    for root, dirs, files in os.walk(Path(path)):
        for file in files:
            list_of_files.append(file)
    return list_of_files


def get_delivery_params(param_string):
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
    options = param_string.get('options')
    new_filename = param_string.get('new_filename')
    return {'transport': transport, 'host': host, 'login': login,
            'password': password, 'key': key, 'folder': folder, 'port': port,
            'local': local, 'id': id, 'remote_file': remote_file, 
            'spool_file': spool_file, 'file': file, 'spool': spool,
            'options': options, 'new_filename': new_filename}

def sendMail(to, fro, subject, text, files=[],server="localhost"):
    assert type(to)==list
    assert type(files)==list


    msg = MIMEMultipart()
    msg['From'] = fro
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(file,"rb").read() )
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                       % os.path.basename(file))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(fro, to, msg.as_string() )
    smtp.close()