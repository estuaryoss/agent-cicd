import re

import requests
from requests.auth import HTTPBasicAuth

from utils.io_utils import IOUtils


class RestApiService:
    def __init__(self, connection):
        self.conn = connection

    def about(self):
        endpoint = "/about"
        url_format = f"{self.conn.get('protocol')}://{self.conn.get('ip')}:{self.conn.get('port')}{endpoint}"
        headers = {
            "Token": self.conn.get('token'),
            "Content-Type": "application/json"
        }

        response = requests.get(url_format, headers=headers, timeout=5, verify=self.conn.get('cert'),
                                auth=HTTPBasicAuth(self.conn.get('username'), self.conn.get('password')))

        if response.status_code != 200:
            raise BaseException("Error: Http code: {}. Http body: {}".format(response.status_code, response.text))

        return response.json()

    def ping(self):
        endpoint = "/ping"
        url_format = f"{self.conn.get('protocol')}://{self.conn.get('ip')}:{self.conn.get('port')}{endpoint}"
        headers = {
            "Token": self.conn.get('token'),
            "Content-Type": "application/json"
        }

        response = requests.get(url_format, headers=headers, timeout=5, verify=self.conn.get('cert'),
                                auth=HTTPBasicAuth(self.conn.get('username'), self.conn.get('password')))

        if response.status_code != 200:
            raise BaseException("Error: Http code: {}. Http body: {}".format(response.status_code, response.text))

        return response.json()

    def post(self, content):
        content = content.strip()
        url_format = f"{self.conn.get('protocol')}://{self.conn.get('ip')}:{self.conn.get('port')}{self.conn.get('endpoint')}"
        headers = {
            "Token": self.conn.get('token'),
            "Content-Type": "application/json"
        }

        response = requests.post(url_format, headers=headers, data=content, timeout=5, verify=self.conn.get('cert'),
                                 auth=HTTPBasicAuth(self.conn.get('username'), self.conn.get('password')))

        if not re.search('^20\d$', str(response.status_code)):
            raise BaseException("Error: Http code: {}. Http body: {}".format(response.status_code, response.text))

        return response.json()

    def get(self):
        endpoint = "/commanddetached"
        url_format = f"{self.conn.get('protocol')}://{self.conn.get('ip')}:{self.conn.get('port')}{endpoint}"
        headers = {
            "Token": self.conn.get('token'),
            "Content-Type": "application/json"
        }

        response = requests.get(url_format, headers=headers, timeout=5, verify=self.conn.get('cert'),
                                auth=HTTPBasicAuth(self.conn.get('username'), self.conn.get('password')))

        # error, server sent non 20x code
        if not re.search('^20\d$', str(response.status_code)):
            return response.json()

        body = response.json()

        # error, the type should be dict
        if isinstance(body['description'], str):
            raise BaseException(body.get('description'))

        return body

    def upload_file(self, remote_path, local_path):
        url_format = f"{self.conn.get('protocol')}://{self.conn.get('ip')}:{self.conn.get('port')}/file"
        headers = {
            "Token": self.conn.get('token'),
            "File-Path": remote_path,
            "Content-Type": "application/octet-stream"
        }
        response = requests.post(url_format, headers=headers, data=IOUtils.read_file(local_path),
                                 verify=self.conn.get('cert'),
                                 auth=HTTPBasicAuth(self.conn.get('username'), self.conn.get('password')))

        # error, server sent non 200 OK response code
        if response.status_code != 200:
            raise BaseException("Error: Http code: {}. Http body: {}".format(response.status_code, response.text))

        body = response.json()

        return {
            "code": 0,
            "out": f"Upload {body.get('description')} from {local_path} to {remote_path}",
            "err": ""
        }

    def download_file(self, remote_path, local_path):
        url_format = f"{self.conn.get('protocol')}://{self.conn.get('ip')}:{self.conn.get('port')}/file"
        headers = {
            "Token": self.conn.get('token'),
            "File-Path": remote_path,
            "Content-Type": "application/octet-stream"
        }
        response = requests.get(url_format, headers=headers, stream=True, verify=self.conn.get('cert'),
                                auth=HTTPBasicAuth(self.conn.get('username'), self.conn.get('password')))
        response.raw.decode_content = True

        # error, server sent non 200 OK response code
        if response.status_code != 200:
            raise BaseException("Error: Http code: {}.".format(response.status_code))
        IOUtils.write_to_file_binary(local_path, raw_response=response.raw)

        return {
            "code": 0,
            "out": f"Saved at location {local_path}",
            "err": ""
        }