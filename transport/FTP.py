import ftplib
import logging
import sys 

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
        self.std_out_bckup = sys.stdout
        self.logger = logging.getLogger(__name__)
        self.logger_connection_handler = logging.FileHandler(self.log_file)
        self.frm = "%(levelname)-.3s [%(asctime)s.%(msecs)03d]  %(name)s: %(message)s"
        self.logger_connection_handler.setFormatter(logging.Formatter(self.frm, "%Y%m%d-%H:%M:%S"))
        self.logger.addHandler(self.logger_connection_handler)
        # self.backup_write = sys.stdout
        
    def _connect(self):
        self.log = open(self.log_file, "a")
        sys.stdout = self.log
        try:
            self.connection.connect(self.host, self.port, timeout=90)
            self.connection.login(self.username, self.password)
            if self.tls:
                self.connection.prot_p()
                self.connection.nlst()
        except Exception as error:
            return error
        finally:
            self.log.flush()
            sys.stdout  = self.std_out_bckup

    def _put(self, local_file, remote_file):
        self.log = open(self.log_file, "a")
        sys.stdout = self.log
        self.connection.storbinary('STOR ' + remote_file, open (local_file, 'rb')) 
        self.log.flush()
        sys.stdout  = self.std_out_bckup

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.log = open(self.log_file, "a")
        sys.stdout = self.log
        self.connection.__exit__(self, *args)
        self.log.flush()
        sys.stdout  = self.std_out_bckup
        self.log.close()