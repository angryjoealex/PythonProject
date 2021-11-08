import logging
import boto3

from contextlib import redirect_stdout

from common import get_path, get_utc_timestamp, get_delivery_params

class S3:
    def __init__(self, delivery, path):
        param = get_delivery_params(delivery)
        self.host = param.get('host')
        self.username = param.get('login')
        self.port = param.get('port')
        self.password = param.get('password')
        self.key = param.get('ftp_identity')
        self.log_file = str(path / 'connection_logs' / str(param.get('id')))
        self.delivery = delivery
        boto3.set_stream_logger('botocore', level=logging.DEBUG)
        self.logger = logging.getLogger('botocore')
        self.logger_connection_handler = logging.FileHandler(self.log_file)
        self.frm = "%(levelname)-.3s [%(asctime)s.%(msecs)03d]  %(name)s: %(message)s"
        self.logger_connection_handler.setFormatter(logging.Formatter(self.frm, "%Y%m%d-%H:%M:%S"))
        self.logger.addHandler(self.logger_connection_handler)

    def _connect(self):
        try:
            self.connection = boto3.client(
                "s3",
                aws_access_key_id = self.username,
                aws_secret_access_key = self.password)
        except Exception as error:
            return error

    def _put(self, local_file, bucket, remote_file):
        self.connection.upload_file(local_file, bucket, remote_file) 

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self