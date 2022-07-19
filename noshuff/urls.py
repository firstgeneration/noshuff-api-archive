from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth', views.pre_auth, name='pre_auth'),
    path('post_auth', views.post_auth, name='post_auth')
]
