import urllib
from django.conf import settings
import requests
import json
import base64
from random import Random


def generate_spotify_auth_url():
    state = int(Random().random() * 10000000000000000)
    scope = 'user-read-private user-read-email'
    url = 'https://accounts.spotify.com/authorize?'
    data = {'client_id': settings.SPOTIFY_CLIENT_ID,
            'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
            'response_type': 'code',
            'scope': scope,
            'state': state}
    query_params = urllib.parse.urlencode(data, doseq=False)

    return url + query_params

def exchange_code_for_token_data(code):
    auth_string = f'{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_SECRET_KEY}'
    auth_string_bytes = auth_string.encode("ascii")
    base64_bytes = base64.b64encode(auth_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    headers = { 'Authorization': f'Basic {base64_string}' }
    data = {'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.SPOTIFY_REDIRECT_URI}
    url = 'https://accounts.spotify.com/api/token'
    query_params = urllib.parse.urlencode(data, doseq=False)

    response = requests.request('GET', url=url, params=query_params, headers=headers)

    return json.loads(response.content)

def fetch_spotify_user_data(spotify_access_token):
    url = 'https://api.spotify.com/v1/me'
    headers = { 'Authorization': f'Bearer {spotify_access_token}' }
    response = requests.request('GET', url=url, headers=headers)
    requests.request()

    return json.loads(response.content)

