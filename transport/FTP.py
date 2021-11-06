import ftplib
from common import get_path, get_utc_timestamp, get_delivery_params

class Ftp:
    def __init__(self, delivery, path):
        param = get_delivery_params(delivery)
        self.host = param.get('host')
        self.username = param.get('login')
        self.port = param.get('port')
        self.password = param.get('password')
        self.key = param.get('ftp_identity')
        self.log_file = str(path / 'connection_logs' / str(param.get('id')))
        self.delivery = delivery
        self.tls = False
        if param.get('options'):
            self.tls = param.get('options').get('TLS', False)
        self.connection = ftplib.FTP()
        if self.tls:
            self.connection = ftplib.FTP_TLS()
        self.connection.set_debuglevel(1)

    def _connect(self):
        try:
            self.connection.connect(self.host, self.port, timeout=90)
            self.connection.login(self.username, self.password)
            if self.tls:
                self.connection.prot_p()
                self.connection.nlst()
        except Exception as error:
            return error

    def _put(self, local_file, remote_file):
        self.connection.storbinary('STOR ' + remote_file, open (local_file, 'rb')) 

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.connection.__exit__(self, *args)