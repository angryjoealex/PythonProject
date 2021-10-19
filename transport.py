import ftplib
import pysftp
from common import get_path, get_utc_timestamp, get_delivery_params


PATH = get_path()


class Transport:
    """Transport for sFTP/FTP/S3"""
    def __init__(self, delivery):
        param = get_delivery_params(delivery)
        self.host = param.get('host')
        self.transport = param.get('transport')
        self.host = param.get('host')
        self.username = param.get('login')
        self.port = param.get('port')
        self.password = param.get('password')
        self.key = param.get('ftp_identity')
        self.log_file = str(PATH / 'connection_logs' / str(param.get('id')))
        self.delivery = delivery
        self.status = []

    def _connect(self):
        if self.transport == 'SFTP':
            self._sftp_connect()
        elif self.transport == 'FTP':
            self._ftp_connect()
        elif self.transport == 'S3':
            self._S3_connect()

    def _sftp_connect(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        cnopts.compression = True
        cnopts.log = self.log_file
        if not self.key:
            self.conn = pysftp.Connection(
                host=self.host,
                username=self.username,
                password=self.password,
                port=self.port,
                cnopts=cnopts)
        else:
            self.conn = pysftp.Connection(
                host=self.host,
                username=self.username,
                private_key=self.key,
                port=self.port,
                cnopts=cnopts)

    def _ftp_connect(self):
        try:
            self.conn.voidcmd("NOOP")
            return True
        except Exception as error:
               return str(error)
        self.conn = ftplib.FTP()
        self.conn.connect(self.host, self.port, timeout=60)
        self.conn.login(self.username, self.password)

    def _s3_connect(self):
        pass

    def put(self):
        """
        Put file from local filesystem to (s)FTP/S3.
        """
        try:
            self._connect()
            with self.conn:
                for task in self.delivery:
                    params = get_delivery_params(task)
                    try:
                        if self.transport == 'SFTP':   
                            self._sftp_put(str(params['spool_file']), params['remote_file'])
                        elif self.transport == 'FTP':
                            self._ftp_put(str(params['spool_file']), params['remote_file'])
                        elif self.transport == 'S3':
                            sftp._s3_put(str(params['spool_file']), params['remote_file'])
                        params.update(status='Completed', last_status_ts=get_utc_timestamp())
                        self.status.append(params)
                    except Exception as error:  # here we catch put failures
                        params.update(status='Error', last_status_ts=get_utc_timestamp(), last_error=str(error))
                        self.status.append(params)
                        continue
        except Exception as error:  # Here we catch connection failures
            err_status = 'Error'
            err_last_status_ts = get_utc_timestamp()
            err_last_error = str(error)
            for task in self.delivery:
                params = get_delivery_params(task)
                params.update(status=err_status, last_status_ts=err_last_status_ts, last_error=err_last_error)
                self.status.append(params)
        return self.status

    def _sftp_put(self, local_file, remote_file):
        self.conn.put(local_file, remote_file)

    def _ftp_put(self, local_file, remote_file):
        file = open(local_file, 'rb')
        self.conn.storbinary(remote_file, file)
        file.close()
