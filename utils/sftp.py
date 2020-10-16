#!/usr/bin/env python3

__author__ = "Catalin Dinuta"


class Sftp:
    """File downloader and uploader similar with transferring files over SSH"""

    @staticmethod
    def upload_file(service, local_path, remote_path):
        return service.upload_file(local_path=local_path, remote_path=remote_path)

    @staticmethod
    def download_file(service, remote_path, local_path):
        return service.download_file(remote_path=remote_path, local_path=local_path)
