import json
import os
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl
import logging

import src.custom_error as ce


def post(event, context):
    logger = logging.getLogger()
    logLevel = logging.INFO

    logger.info(event)

    API_KEY = os.environ['API_KEY']
    API_SECRET = os.environ['API_SECRET']
    access_token_url = 'https://api.twitter.com/oauth/access_token'

    if 'body' not in event:
        logger.error('400 No body')
        raise ce.CustomError(400, 'No body')

    request_body = json.loads(event['body'])

    if 'oauth_token' not in request_body or 'oauth_verifier' not in request_body:
        logger.error('400 No params')
        raise ce.CustomError(400, 'No params')

    oauth_token = request_body['oauth_token']
    oauth_verifier = request_body['oauth_verifier']

    try:
        twitter = OAuth1Session(API_KEY, API_SECRET, oauth_token, oauth_verifier)

        twitter_response = twitter.post(
            access_token_url,
            params={'oauth_verifier': oauth_verifier}
        )

        access_token = dict(parse_qsl(twitter_response.content.decode('utf-8')))
    except Exception as e:
        logger.error(e)
        raise ce.CustomError(500, 'Twitter Error')

    if access_token == {}:
        logger.error("401 Can't get access_token")
        raise ce.CustomError(401, "Can't get access_token")

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Access-Control-Allow-Origin'
    }
    body = {
        'access_token': access_token,
    }

    logger.info(body)

    response = {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(body)
    }
    return response
