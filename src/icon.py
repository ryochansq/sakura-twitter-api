import json
import os


def main(event, context):
    body = {
        'key': os.environ['CONSUMER_KEY'],
        'secret': os.environ['CONSUMER_SECRET']
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
