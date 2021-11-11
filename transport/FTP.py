import ftplib
import logging
import sys 

from contextlib import redirect_stdout
from pathlib import PurePosixPath

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
        self.logger = logging.getLogger(__name__)
        self.logger_connection_handler = logging.FileHandler(self.log_file)
        self.frm = "%(levelname)-.3s [%(asctime)s.%(msecs)03d]  %(name)s: %(message)s"
        self.logger_connection_handler.setFormatter(logging.Formatter(self.frm, "%Y%m%d-%H:%M:%S"))
        self.logger.addHandler(self.logger_connection_handler)
        self.logger.write = lambda msg: self.logger.debug(msg) if msg != '\n' else None
        
    def _connect(self):
        with redirect_stdout(self.logger):
            try:
                self.connection.connect(self.host, self.port, timeout=90)
                self.connection.login(self.username, self.password)
                if self.tls:
                    self.connection.prot_p()
                    self.connection.nlst()
            except Exception as error:
                return error

    def _put(self, local_file, remote_file):
        with redirect_stdout(self.logger):
            if not remote_file.startswith("/"): # normalize path
                remote_file = "/" + remote_file
            remote_directory = str(PurePosixPath(remote_file).parent)
            self._ftp_mkdirs(remote_directory)
            self.connection.cwd("/")
            self.connection.storbinary('STOR ' + remote_file, open (local_file, 'rb')) 

    def _ftp_mkdirs(self, folder):
        # create paths if do not exists
        for subfolder in folder.split('/'):
            if subfolder and subfolder not in self.connection.nlst():
                self.connection.mkd(subfolder)
            self.connection.cwd(subfolder)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        with redirect_stdout(self.logger):
            self.connection.__exit__(self, *args)