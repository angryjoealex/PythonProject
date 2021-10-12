import datetime
import os
import pathlib
from datetime import timezone


def get_path():
    path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
    return path


def get_utc_timestamp():
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = str(utc_time.timestamp()).replace('.', '')
    return utc_timestamp
