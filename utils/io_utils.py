import errno
import os
import shutil
from pathlib import Path


class IOUtils:
    @staticmethod
    def read_file(file):
        file_path = Path(file)
        if not file_path.is_file():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
        with open(file, 'rb') as f:
            return f.read()

    @staticmethod
    def write_to_file_binary(file, raw_response):
        with open(file, 'wb') as f:
            shutil.copyfileobj(raw_response, f)
