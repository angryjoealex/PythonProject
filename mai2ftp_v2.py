import sys
import mailparser
import logging
import re
from ast import literal_eval
import pathlib
from datetime import timezone
import datetime
import csv
import os
from sqlalchemy import create_engine

PATH = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
SPOOL_PATH = PATH / 'spool'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.ERROR,
                    filename=PATH / 'mail2_ftp2.log')


# get UTC timestamp
def get_utc_timestamp():
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = str(utc_time.timestamp()).replace('.', '')
    return utc_timestamp


def remove_file(path_to_file):
    pathlib.Path.unlink(path_to_file)


def get_delivery_params(param_string):
    transport = None
    host = None
    login = None
    password = None
    identity = None
    remote_dir = None
    try:
        transport = param_string['transport']
    except KeyError:
            print('Transport is not defined')
    try:
        host = param_string['host']
    except KeyError:
        print('Host is not defined')
    try:
        login = param_string['login']
    except KeyError:
        print('Login is not defined')
    try:
        login = param_string['folder']
    except KeyError:
        print('Remote directory is not defined')
    try:
        password = param_string['password']
        if not param_string['password']:
            try:
                identity = param_string['ftp_identity']
            except KeyError:
                print('No password or key file is defined')
    except KeyError:
        print('No password or key file is defined')
    return transport, host, login, password, identity, remote_dir


def main(raw_email):
    delivery = []
    # Parse email from file  and delete raw email
    mail = mailparser.parse_from_file(raw_email)
    remove_file(raw_email)
    # Get POSTFIX mail ID
    for received in mail.received:
        try:
            received['with']
            received_id_posfix = received['id']
        except KeyError:
            pass  # there are 2 received: host to gateway, gateway to script. We get data from host to gateway received
    #create spool folder for POSTFIX mail ID
    spool_path_file = SPOOL_PATH / received_id_posfix
    try:
        pathlib.Path(spool_path_file).mkdir(parents=True, exist_ok=True)
        # Save email body
        with open(spool_path_file / 'message', 'w+') as message_body:
            message_body.write(mail.body)
    except PermissionError as error:
        print(f"Can't write email body.\n {error}")
        return
    # get params for delivery
    get_param = re.search('mail2ftp:\{.+\}', mail.body)
    try:
        get_param.group(0)
    except AttributeError:
        print('No deilvery parameters are defined')
        return
    params = get_param.group(0).replace('mail2ftp:', '')
    params = re.sub(r"(\w+): ", r"'\1':", params).replace(' ', '')
    # convert to dict
    upload_creds = literal_eval(params)
    # get delivery params
    transport, host, login, password, identity, remote_dir = get_delivery_params(upload_creds)
    # if deined delivery params, save attach
    if not (transport and host and remote_dir and (password or identity)):
        print(f"Delivery params are not fully defined transport: {transport}, host: {host}, password: {password}, identity: {identity} ")
        return
    # Save attached files and populate delivery parameters
    for attach in mail.attachments:
        attached_file_w_path = ''
        filename = re.search('filename=".*"', attach['content-disposition'].replace('\n',' '))
        try:
            filename.group(0)
            filename = filename.group(0).replace('filename=','').replace('"','')
            attached_file_w_path = SPOOL_PATH / received_id_posfix / filename
        except IndexError:
            print("Can't get attach name")
            return
    # write attach to spool and polpulate variable
        try:
            mail.write_attachments(SPOOL_PATH/received_id_posfix)
        except PermissionError as error:
            print(f"{error}.\n Can't write attached file")
            return
        delivery.append({'transport': transport, 'host': host,'login': login,'password': password,'identity': identity, 'file': attached_file_w_path})
    # test - write delivery par to csv
    param_out = SPOOL_PATH / received_id_posfix / 'delivery.csv'
    headers = delivery[0].keys()
    with open(param_out, mode="w+", encoding='utf-8') as param_file:
        file_writer = csv.DictWriter(param_file, headers, delimiter=";", lineterminator="\r")
        file_writer.writeheader()
        file_writer.writerows(delivery)


utc_ts = get_utc_timestamp()
raw_email = SPOOL_PATH / utc_ts

# Read mail from POSTFIX
data = sys.stdin.read()
try:
    with open(raw_email, 'w+') as file:
        file.write(data)
except (FileNotFoundError, PermissionError) as error:
    print(f"{error}\nCan't write raw email")

main(raw_email)
