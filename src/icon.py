import json
import os
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl


def get(event, context):
    body = {
        'key': os.environ['API_KEY'],
        'secret': os.environ['API_SECRET']
    }
    response = {
        "statusCode": 200,
        "body": 'ok'
    }
    return response
