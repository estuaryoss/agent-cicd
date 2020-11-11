import errno
import os
import shutil
from pathlib import Path


class IOUtils:

    @staticmethod
    def create_dir(path, permissions=0o755):
        if not os.path.exists(path):
            os.makedirs(path, permissions)

    @staticmethod
    def read_file(file, type='rb'):
        if not Path(file).is_file():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), Path(file))
        with open(file, type) as f:
            return f.read()

    @staticmethod
    def get_fh_for_read(file):
        if not Path(file).is_file():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), Path(file))
        return open(file, 'r')

    @staticmethod
    def write_to_file_binary(file, raw_response):
        with open(file, 'wb') as f:
            shutil.copyfileobj(raw_response, f)

    @staticmethod
    def write_to_file(file, content=""):
        with open(file, 'w') as f:
            f.write(content)
