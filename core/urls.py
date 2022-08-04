from django.urls import path
from core.authentication import views as auth_views

urlpatterns = [
    path('auth', auth_views.pre_auth, name='pre_auth'),
    path('post_auth', auth_views.post_auth, name='post_auth')
]
