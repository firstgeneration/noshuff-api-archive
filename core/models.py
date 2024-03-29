from re import T
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import jwt
import datetime
import requests
from base64 import b64encode
from django_extensions.db.models import TimeStampedModel


class User(AbstractUser):
    id = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    avatar_url = models.URLField(null=True)
    spotify_access_token = models.CharField(max_length=100, null=True, blank=True)
    spotify_refresh_token = models.CharField(max_length=100, null=True, blank=True)

    @staticmethod
    def get_user_from_auth_token(token):
        decoded = User.decode_auth_token(token)
        id = decoded['id']
        return User.objects.filter(id=id).first()

    @staticmethod
    def decode_auth_token(token):
        # Add in error handling
        return jwt.decode(token, settings.JWT_SECRET, algorithms='HS256')

    def generate_auth_token(self, expires_in=360):
        return jwt.encode(
            {
                'id': self.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=int(expires_in)),
            },
            settings.JWT_SECRET,
            algorithm='HS256'
        )

    def generate_auth_token(self, expires_in=360):
        return jwt.encode(
            {
                'id': self.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=int(expires_in)),
            },
            settings.JWT_SECRET,
            algorithm='HS256'
        )

    def get_new_token(self):
        url = 'https://accounts.spotify.com/api/token'
        auth_string = f'Basic {settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_SECRET_KEY}'
        headers = { 'Authorization': b64encode(auth_string)}
        data = {'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token}

        response = requests.request('GET', url=url, headers=headers, data=data)

        # handle new token failure

        token_json = response.json()

        self.spotify_access_token = token_json['access_token']
        self.scope = token_json['scope']
        self.save()


class Post(TimeStampedModel):
    # uuid = 
    spotify_playlist_id = models.CharField(max_length=64)
    # name = models.CharField(max_length=64)
    caption = models.CharField(max_length=144)
    # playlist cover image(s) - consider an array field here for the urls
    # track_count = models.IntegerField() - This may become stale, could use a lazy-update 
    # duration (v2) - See if there is a field for storing a duration - similar issue with track_count

    # Relations
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    # tags = models.ManyToManyField('HashTag', on_delete=models.CASCADE)


class HashTag(TimeStampedModel):
    # uuid = 
    # tag = models.CharField(null=False, unique=True)
    pass


class Like(TimeStampedModel):
    pass
    # uuid = 
    # liker = models.ForeignKey('User', on_delete=models.CASCADE) 
    # post = models.ForeignKey('Post', on_delete=models.CASCADE)


class Comment(TimeStampedModel):
    # uuid = 
    text = models.TextField()
    
    # Realtions
    # author = models.ForeignKey('User', on_delete=models.CASCADE)
    # post = models.ForeignKey('Post', on_delete=models.CASCADE)
    
    # For nested comments - use POSTGRES BTREE
    # parent = models.ForeignKey('Comment', on_delete=models.CASCADE)
