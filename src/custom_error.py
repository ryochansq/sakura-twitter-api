import json


class CustomError(Exception):
    def __init__(self, code, messages):
        self.code = code
        self.messages = messages

    def __str__(self):
        response = {
            'status': 'HTTP/1.1 {0} Error'.format(self.code),
            'statusCode': self.code,
            'headers': {
                'Content-Type': 'application/octet-stream',
                'Accept-Charset': 'UTF-8'
            },
            'body': {
                'errorMessage': self.messages
            }
        }
        return json.dumps(response)
