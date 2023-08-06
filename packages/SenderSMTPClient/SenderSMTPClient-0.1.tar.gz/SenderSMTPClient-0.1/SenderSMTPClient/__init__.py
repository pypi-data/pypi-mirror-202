import requests

__version__ = "0.1"


class SenderSMTPClient:
    def __init__(self, dsn: str, secret_key: str, project_id: str, content_type: str = 'html', timeout: int = 10):
        self.dsn = dsn
        self.secret_key = secret_key
        self.project_id = project_id
        self.content_type = content_type
        self.timeout = timeout

        self.headers = {
            'X-Secret-Key': self.secret_key,
            'X-Project-ID': self.project_id,
        }

    def get_response(self, response):
        return response

    def send(self, subject: str, message: str, to: str):
        message = {
            'subject': subject,
            'message': message,
            'to': to,
            'content-type': self.content_type,
        }
        response = requests.post(
            self.dsn, headers=self.headers, json=message, verify=False, timeout=self.timeout)

        return self.get_response(response.json())
