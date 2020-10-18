import base64
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
    post_media_url = 'https://upload.twitter.com/1.1/media/upload.json'
    post_tweet_url = 'https://api.twitter.com/1.1/statuses/update.json'

    if 'body' not in event:
        logger.error('400 No body')
        raise ce.CustomError(400, 'No body')

    request_body = json.loads(event['body'])

    if 'image' not in request_body or 'access_token' not in request_body:
        logger.error('400 No params')
        raise ce.CustomError(400, 'No params')

    access_token = request_body['access_token']

    # base64形式のraw_imageの先頭の'data:image/png;base64,'を削除
    raw_image = request_body['image']
    image = raw_image[22:]

    try:
        oauth_token = access_token['oauth_token']
        oauth_token_secret = access_token['oauth_token_secret']
        user_id = access_token['user_id']
        screen_name = access_token['screen_name']

        twitter = OAuth1Session(API_KEY, API_SECRET, oauth_token, oauth_token_secret)

        # 画像をアップロード
        files = {'media_data': image}

        media_response = twitter.post(post_media_url, files=files)
        media = json.loads(media_response.text)
        media_id = media['media_id']
    except Exception as e:
        logger.error(e)
        raise ce.CustomError(500, 'Twitter media Error')

    try:
        # ツイート
        message = '''生徒証メーカーで生徒証を作りました！

▼生徒証メーカー
https://ryochansq.github.io/sakura-card-maker/

#さくら学院 #生徒証メーカー'''

        params = {
            'status': message,
            'media_ids': [media_id]
        }

        tweet_response = twitter.post(post_tweet_url, params=params)
    except Exception as e:
        logger.error(e)
        raise ce.CustomError(500, 'Twitter tweet Error')

    logger.info('tweet complete')

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Access-Control-Allow-Origin'
    }
    response = {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({})
    }
    return response
