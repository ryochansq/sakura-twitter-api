import json
import os
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl


def post(event, context):
    API_KEY = os.environ['API_KEY']
    API_SECRET = os.environ['API_SECRET']
    get_user_url = 'https://api.twitter.com/1.1/users/show.json'

    request_body = json.loads(event['body'])
    access_token = request_body['access_token']

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

    body = {
        'profile_image_url': profile_image_url
    }
    response = {
        'statusCode': 200,
        'body': json.dumps(body)
    }
    return response
