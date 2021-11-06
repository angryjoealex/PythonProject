import pysftp
from pysftp import exceptions

from common import get_path, get_utc_timestamp, get_delivery_params

class Sftp:
    def __init__(self, delivery, path):
        param = get_delivery_params(delivery)
        self.host = param.get('host')
        self.username = param.get('login')
        self.port = param.get('port')
        self.password = param.get('password')
        self.key = param.get('ftp_identity')
        self.log_file = str(path / 'connection_logs' / str(param.get('id')))
        self.delivery = delivery

        self.cnopts = pysftp.CnOpts()
        self.cnopts.hostkeys = None
        self.cnopts.compression = True
        if param.get('options'):
            self.cnopts.compression = param.get('options').get('Compression', True)
        self.cnopts.log = self.log_file
    
    def _connect(self):
        try:
            if not self.key:
                self.connection = pysftp.Connection(
                    host=self.host,
                    username=self.username,
                    password=self.password,
                    port=self.port,
                    cnopts=self.cnopts)
            else:
                self.connection = pysftp.Connection(
                    host=self.host,
                    username=self.username,
                    private_key=self.key,
                    port=self.port,
                    cnopts=self.cnopts)
        except exceptions.ConnectionException as error:
            return (f"The host is not available {error}")
        except Exception as error:
            return error

    def _put(self, local_file, remote_file):
        self.connection.put(local_file, remote_file, confirm=False)  # disable check if file were uploaded or not

    def __enter__(self):
        return self

    def __exit__(self, etype, value, traceback):
       self.connection.close()