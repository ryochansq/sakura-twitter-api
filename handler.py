import json


def hello(event, context):
    body = {
        'hoge': 'hello'
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response


def hello2(event, context):
    body = {
        'hoge': 'hello2'
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
