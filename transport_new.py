import ftplib
import pysftp
from common import get_path, get_utc_timestamp, get_delivery_params
# from .transport.SFTP import Sftp

from transport.SFTP import Sftp
from transport.FTP import Ftp

PATH = get_path()


class Transport:
    """Transport for sFTP/FTP/S3"""
    def __init__(self, delivery):
        param = get_delivery_params(delivery)
        self.transport = param.get('transport')
        self.delivery = delivery
        self.status = []

    def _connect(self):
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
        try:
            self._connect()
            with self.connection:
                for task in self.delivery:
                    params = get_delivery_params(task)
                    try:
                        self.connection._put(str(params['spool_file']), params['remote_file'])
                        params.update(status='Completed', last_status_ts=get_utc_timestamp(), next_attempt=None)
                        self.status.append(params)
                    except Exception as error:  # here we catch put failures
                        params.update(status='Error', last_status_ts=get_utc_timestamp(), last_error=str(error), next_attempt=None)
                        self.status.append(params)
                        continue
        except Exception as error:  # Here we catch connection failures
            err_status = 'Error'
            err_last_status_ts = get_utc_timestamp()
            err_last_error = str(error)
            for task in self.delivery:
                params = get_delivery_params(task)
                params.update(status=err_status, last_status_ts=err_last_status_ts, last_error=err_last_error, next_attempt=None)
                self.status.append(params)
        return self.status

