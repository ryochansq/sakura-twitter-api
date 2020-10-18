import json
import os
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl
import logging

import src.custom_error as ce


def get(event, context):
    logger = logging.getLogger()
    logLevel = logging.INFO

    logger.info(event)

    API_KEY = os.environ['API_KEY']
    API_SECRET = os.environ['API_SECRET']
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    oauth_callback = 'https://ryochansq.github.io/sakura-card-maker/edit'

    try:
        twitter = OAuth1Session(API_KEY, API_SECRET)

        response = twitter.post(
            request_token_url,
            params={'oauth_callback': oauth_callback}
        )

        # responseからリクエストトークンを取り出す
        request_token = dict(parse_qsl(response.content.decode('utf-8')))

        # リクエストトークンから連携画面のURLを生成
        authenticate_url = 'https://api.twitter.com/oauth/authenticate'
        authenticate_endpoint = '%s?oauth_token=%s' % (authenticate_url, request_token['oauth_token'])
    except Exception as e:
        logger.error(e)
        raise ce.CustomError(500, 'Twitter Error')

    headers = {
        'Access-Control-Allow-Origin': '*',
    }
    body = {
        'authenticate_endpoint': authenticate_endpoint
    }

    logger.info(body)

    response = {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(body)
    }
    return response
