import datetime
import os
import pathlib
import sys
import smtplib
import socket

from datetime import timezone
from pathlib import Path

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

from sqlalchemy.sql.operators import from_

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
    failyre_reply = param_string.get('onFailure')
    succes_reply = param_string.get('onSucces')
    return {'transport': transport, 'host': host, 'login': login,
            'password': password, 'key': key, 'folder': folder, 'port': port,
            'local': local, 'id': id, 'remote_file': remote_file, 
            'spool_file': spool_file, 'file': file, 'spool': spool,
            'options': options, 'new_filename': new_filename,
            'failyre_reply': failyre_reply, 'succes_reply': succes_reply}


def send_mail(to, subject, text, files=None, server="localhost", port =1025):
    status = None
    if not isinstance(to, list):
        if isinstance(to, str):
            to = list(to.strip().split(','))
        else:
            status = {'type': 'error', 'msg':'email address is not properly defined'}
            return status  
    if files:
        if not isinstance(files, list):
            if isinstance(to, str):
                to = list(to.strip().split(','))
            else:
                status = {'type': 'error', 'msg':'file path is not properly defined'}
                return status  
    
    msg = MIMEMultipart()
    msg['From'] = socket.gethostname() # get host name where the script runs
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach( MIMEText(text) )
    if files:
        try:
            for file in files:
                part = MIMEBase('application', "octet-stream")
                part.set_payload( open(file,"rb").read() )
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"'
                            % os.path.basename(file))
                msg.attach(part)
        except Exception as error:
            status = {'type': 'error', 'msg':{error}}
            return status

    smtp = smtplib.SMTP(server, port)
    smtp.sendmail(socket.gethostname(), to, msg.as_string() )
    smtp.close()
    status = {'type': 'success', 'msg':'email has been succesfully sent'}
    return status
