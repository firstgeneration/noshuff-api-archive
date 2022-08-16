from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class ListUserPlaylists(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth())

        playlists = sp.user_playlists(username)

        for playlist in playlists['items']:
            print(playlist['name'])
        return Response()

