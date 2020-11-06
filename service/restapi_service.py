import requests


class RestApiService:
    def __init__(self, connection):
        self.conn = connection

    def ping(self):
        endpoint = "/ping"
        url_format = f"{self.conn.get('protocol')}://{self.conn.get('ip')}:{self.conn.get('port')}{endpoint}"
        headers = {
            "Token": self.conn.get('token'),
            "Content-Type": "application/json"
        }

        response = requests.get(url_format, headers=headers, timeout=5, verify=self.conn.get('cert'))

        return response.json()

    def post(self, content):
        content = content.strip()
        url_format = f"{self.conn.get('protocol')}://{self.conn.get('ip')}:{self.conn.get('port')}{self.conn.get('endpoint')}"
        headers = {
            "Token": self.conn.get('token'),
            "Content-Type": "application/json"
        }

        response = requests.post(url_format, headers=headers, data=content, timeout=5, verify=self.conn.get('cert'))

        return response.json()

    def get(self):
        endpoint = "/commanddetached"
        url_format = f"{self.conn.get('protocol')}://{self.conn.get('ip')}:{self.conn.get('port')}{endpoint}"
        headers = {
            "Token": self.conn.get('token'),
            "Content-Type": "application/json"
        }

        response = requests.get(url_format, headers=headers, timeout=5, verify=self.conn.get('cert'))

        # error, server sent non 202 ACCEPTED code
        if response.status_code != 202:
            return response.json()

        body = response.json()

        # error, the type should be dict
        if isinstance(body['description'], str):
            raise body.get('description')

        return body.get('description')
