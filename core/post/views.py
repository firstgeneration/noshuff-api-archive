from re import M
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotify_utils import DjangoCacheHandler

@api_view(['GET'])
# @authentication_classes()
def get_current_user_unposted_playlists(self, request, format=None):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(),
                         cache_handler=DjangoCacheHandler())

    playlists = sp.current_user_playlists()

    current_user = None # TODO
    current_user.posts_set.values('spotify_playlist_id') # or whatever it's called
    unposted_playlists = {}
    # Parse these playlists
        # remove ones already posted to noshuff

    # for playlist in playlists['items']:
    #     print(playlist['name'])

    return Response(unposted_playlists)


class ListUserSpotifyPlaylists(APIView):

    # Create an authentication class
    # authentication_classes = [MakeThisClass]
    
    # Permissions might not be needed
    # permission_classes = [permissions.IsAdminUser]
    def post()