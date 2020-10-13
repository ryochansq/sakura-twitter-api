import json


def post(event, context):
    body = {
        'hoge': 'hello'
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
