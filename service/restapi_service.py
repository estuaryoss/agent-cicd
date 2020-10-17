import requests


class RestApiService:
    def __init__(self, connection):
        self.conn = connection

    def ping(self):
        endpoint = "/ping"
        url_format = f"{self.conn.get('protocol')}://{self.conn.get('ip')}:{self.conn.get('port')}{endpoint}"
        headers = {
            "Token": self.conn.get('token'),
            "Content-Type": "text/plain"
        }

        response = requests.get(url_format, headers=headers, timeout=5, verify=self.conn.get('cert'))

        if response.status_code != 200:
            return "Error: Http code: {}. Http body: {}".format(response.status_code, response.text)

        return response.json().get('description')

    def post(self, content):
        content = content.strip()
        url_format = f"{self.conn.get('protocol')}://{self.conn.get('ip')}:{self.conn.get('port')}{self.conn.get('endpoint')}"
        headers = {
            "Token": self.conn.get('token'),
            "Content-Type": "text/plain"
        }

        response = requests.post(url_format, headers=headers, data=content, timeout=5, verify=self.conn.get('cert'))

        # error, server sent non 200 OK description code
        if response.status_code != 200:
            return "Error: Http code: {}. Http body: {}".format(response.status_code, response.text)

        try:
            cmds_id = response.json().get('description')
        except Exception as e:
            return "\nError: ({})".format(e.__str__())

        return cmds_id

    def get(self):
        endpoint = "/commanddetached"
        url_format = f"{self.conn.get('protocol')}://{self.conn.get('ip')}:{self.conn.get('port')}{endpoint}"
        headers = {
            "Token": self.conn.get('token'),
            "Content-Type": "text/plain"
        }

        response = requests.get(url_format, headers=headers, timeout=5, verify=self.conn.get('cert'))

        # error, server sent non 200 OK description code
        if response.status_code != 200:
            return "Error: Http code: {}. Http body: {}".format(response.status_code, response.text)

        body = response.json()

        # error, the type should be dict
        if isinstance(body['description'], str):
            raise body.get('description')

        return body.get('description')
