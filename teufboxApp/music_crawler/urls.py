from django.urls import path

from .views import index, search_song, downloader, music_cache

urlpatterns = [
    path('', index, name='index'),
    path('search_song', search_song, name="search_song"),
    path('downloader', downloader, name="downloader"),
    path('music_cache', music_cache, name="music_cache"),
]