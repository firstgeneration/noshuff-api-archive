from django.shortcuts import redirect
from django.conf import settings
from random import Random
import requests
from core.models import User
import urllib
import json


def pre_auth(request):
    state = int(Random().random() * 10000000000000000)
    scope = 'user-read-private user-read-email'
    url = 'https://accounts.spotify.com/authorize?'
    data = {'client_id': settings.SPOTIFY_CLIENT_ID,
            'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
            'response_type': 'code',
            'scope': scope,
            'state': state}

    query_params = urllib.parse.urlencode(data, doseq=False)

    return redirect(url + query_params)

def _fetch_spotify_user_data(spotify_access_token):
    url = 'https://api.spotify.com/v1/me'
    headers = { 'Authorization': f'Bearer {spotify_access_token}' }
    response = requests.request('GET', url=url, headers=headers)

    return json.loads(response.content)

def _exchange_code_for_token_data(code):
    data = {'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.SPOTIFY_REDIRECT_URI}
    query_params = urllib.parse.urlencode(data, doseq=False)

    response = requests.request('GET', url=spotify_token_url + query_params)
    return response.GET

def post_auth(request):
    code_data = request.GET

    error = code_data.get('error')
    if error:
        return redirect(f'{settings.NOSHUFF_FE_REDIRECT_URI}?error={error}')

    token_data = _exchange_code_for_token_data(code_data['code'])
    spotify_access_token = token_data['access_token']
    scope = token_data['scope']
    spotify_access_token_expires_in = token_data['expires_in']
    spotify_refresh_token = token_data['refresh_token']

    spotify_user_data = _fetch_spotify_user_data(spotify_access_token)
    spotify_id = spotify_user_data.get('id')
    email = spotify_user_data.get('email')
    display_name = spotify_user_data.get('display_name')
 
    try:
        avatar_url = spotify_user_data['images'][0]['url']
    except:
        avatar_url = ''

    noshuff_user = User.objects.filter(id=spotify_id).first()
    # Check for inactive so no db failure
    if not noshuff_user:
        noshuff_user = User.objects.create(
            id=spotify_id,
            spotify_access_token=spotify_access_token,
            spotify_refresh_token=spotify_refresh_token,
            display_name=display_name,
            email=email,
            avatar_url=avatar_url)
    else:
        changed = False
        user_data = {'display_name': display_name,
                     'email': email,
                     'avatar_url': avatar_url}

        for attr, val in user_data.items():
            if getattr(noshuff_user, attr) != val:
                changed = True
                setattr(noshuff_user, attr, val)

        if changed:
            noshuff_user.save()

    noshuff_access_token = noshuff_user.generate_auth_token()

    data = {'noshuff_access_token': noshuff_access_token,
            'user_id': noshuff_user.id,
            'display_name': noshuff_user.display_name,
            'avatar_url': noshuff_user.avatar_url}

    query_params = urllib.parse.urlencode(data, doseq=False)

    return redirect(settings.NOSHUFF_FE_REDIRECT_URI + '?' + query_params)

# consider a cookie listener - this will update the state
