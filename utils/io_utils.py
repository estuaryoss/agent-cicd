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

    @staticmethod
    def delete_file(file):
        file_path = Path(file)
        if file_path.is_file():
            try:
                file_path.unlink()
            except Exception as e:
                print(f"Failed to delete file {file}: {e.__str__()}")

    @staticmethod
    def delete_files(files):
        for file in files:
            IOUtils.delete_file(file)

    @staticmethod
    def create_files(files):
        for file in files:
            IOUtils.create_file(file)

    @staticmethod
    def create_file(file):
        file = Path(file)
        file.touch() if not file.exists() else None

    @staticmethod
    def recreate_files(files):
        for file in files:
            IOUtils.delete_file(file)
            IOUtils.create_file(file)
