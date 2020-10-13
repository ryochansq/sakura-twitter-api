import json
import os
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl


def post(event, context):
    API_KEY = os.environ['API_KEY']
    API_SECRET = os.environ['API_SECRET']
    access_token_url = 'https://api.twitter.com/oauth/access_token'

    request_body = json.loads(event['body'])

    oauth_token = request_body['oauth_token']
    oauth_verifier = request_body['oauth_verifier']

    twitter = OAuth1Session(
        API_KEY,
        API_SECRET,
        oauth_token,
        oauth_verifier,
    )

    twitter_response = twitter.post(
        access_token_url,
        params={'oauth_verifier': oauth_verifier}
    )

    access_token = dict(parse_qsl(twitter_response.content.decode("utf-8")))

    body = {
        'access_token': access_token,
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
