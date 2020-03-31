from django.urls import path

from .views import index, search_song, register_song

urlpatterns = [
    path('', index, name='index'),
    path('search_song', search_song, name="search_song"),
    path('register_song', register_song, name="register_song")
]