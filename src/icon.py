import json
import os
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl
import logging
import base64
import requests

import src.custom_error as ce


def post(event, context):
    logger = logging.getLogger()
    logLevel = logging.INFO

    logger.info(event)

    API_KEY = os.environ['API_KEY']
    API_SECRET = os.environ['API_SECRET']
    get_user_url = 'https://api.twitter.com/1.1/users/show.json'

    if 'body' not in event:
        logger.error('400 No body in event')
        raise ce.CustomError(400, 'No body in event')

    request_body = json.loads(event['body'])
    access_token = request_body['access_token']

    if 'access_token' not in request_body:
        logger.error('400 No access_token in body')
        raise ce.CustomError(400, 'No access_token in body')

    try:
        oauth_token = access_token['oauth_token']
        oauth_token_secret = access_token['oauth_token_secret']
        user_id = access_token['user_id']
        screen_name = access_token['screen_name']

        twitter = OAuth1Session(API_KEY, API_SECRET, oauth_token, oauth_token_secret)

        params = {
            'user_id': user_id,
            'screen_name': screen_name
        }

        twitter_response = twitter.get(get_user_url, params=params)
        user = json.loads(twitter_response.text)

        # profile_image_url_httpsの末尾の「_normal」を削除して、originalサイズのURLを生成
        root, ext = os.path.splitext(user['profile_image_url_https'])
        profile_image_url = root[0:-7] + ext

        icon_data = base64.b64encode(requests.get(profile_image_url).content)
        icon64 = 'data:image/png;base64,' + icon_data.decode('utf-8')

    except Exception as e:
        logger.error(e)
        raise ce.CustomError(500, 'Twitter Error')

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Access-Control-Allow-Origin'
    }
    body = {
        'icon': icon64
    }

    logger.info(body)

    response = {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(body)
    }
    return response
