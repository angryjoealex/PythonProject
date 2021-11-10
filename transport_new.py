import logging
import ftplib
import pysftp

from pysftp import exceptions

from common import get_path, get_utc_timestamp, get_delivery_params

from transport.SFTP import Sftp
from transport.FTP import Ftp
from transport.S3 import S3

PATH = get_path()


class Transport:
    """Transport for sFTP/FTP/S3"""
    def __init__(self, delivery):
        self.param = get_delivery_params(delivery)
        self.transport = self.param.get('transport')
        self.delivery = delivery
        self.status = []
        self.logger = logging.getLogger(__name__)
        self.logger_connection_handler = logging.FileHandler(PATH / 'connection_logs' / str(self.param.get('id')))
        self.frm = "%(levelname)-.3s [%(asctime)s.%(msecs)03d]  %(name)s: %(message)s"
        self.logger_connection_handler.setFormatter(logging.Formatter(self.frm, "%Y%m%d-%H:%M:%S"))
        self.logger.addHandler(self.logger_connection_handler)
        


    def _connection(self):
        if self.transport == 'SFTP':
            self.connection = Sftp(self.delivery, PATH)
        elif self.transport == 'FTP':
            self.connection = Ftp(self.delivery, PATH)
        elif self.transport == 'S3':
            self.connection = S3(self.delivery, PATH)

    def put(self):
        """
        Put file from local filesystem to (s)FTP/S3.
        """
        self._connection()
        self.logger.info(f"Going to connect {self.param.get('transport')} {self.param.get('login')}:{self.param.get('password')}@{self.param.get('host')}:{self.param.get('port')}")
        try:
            self.connected = self.connection._connect()
            if self.connected:
                self.logger.info(f"FAILED to connect {self.param.get('transport')} {self.param.get('login')}:{self.param.get('password')}@{self.param.get('host')}:{self.param.get('port')} Error:{self.connected}")
                raise Exception(self.connected)
            self.logger.info(f"Connected to connect {self.param.get('transport')} {self.param.get('login')}:{self.param.get('password')}@{self.param.get('host')}:{self.param.get('port')}")
            with self.connection:
                for task in self.delivery:
                    params = get_delivery_params(task)
                    self.logger.info(f"Going to upload {str(params['spool_file'])} to {self.param.get('host')}\{params['remote_file']}")
                    try:
                        self.connection._put(str(params['spool_file']), params['remote_file'])
                        params.update(status='Completed', last_status_ts = get_utc_timestamp(), next_attempt=None)
                        self.status.append(params)
                        self.logger.info(f"UPLOADED {str(params['spool_file'])} to {self.param.get('host')}\{params['remote_file']}")
                    except Exception as error:  # here we catch put failures
                        params.update(status='Error', last_status_ts = get_utc_timestamp(), last_error=str(error), next_attempt=None)
                        self.status.append(params)
                        self.logger.info(f"FAILED to upload {str(params['spool_file'])} to {self.param.get('host')}\{params['remote_file']}")
                        self.logger.info(str(error))
                        continue
        except Exception as error:  # Here we catch connection failures
            err_status = 'Error'
            err_last_status_ts = get_utc_timestamp()
            err_last_error = str(error)
            for task in self.delivery:
                params = get_delivery_params(task)
                params.update(status = err_status, last_status_ts = err_last_status_ts, last_error = err_last_error, next_attempt = None)
                self.status.append(params)