import os

import googleapiclient.discovery
import googleapiclient.errors

from django.shortcuts import render
from django.http import JsonResponse
from youtube_dl.utils import DownloadError

from .models import Music, Artist
from .utils import download_from_youtube


def index(request):
    return render(request, 'music_crawler/index.html', locals())

def search_song(request):
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv("GOOGLE_KEY")

    youtube = googleapiclient.discovery.build(api_service_name,
                                              api_version,
                                              developerKey=DEVELOPER_KEY)

    # Now that api is authenticated, start process
    keywords = request.GET['keywords']
    yt_request = youtube.search().list(
        part="snippet",
        maxResults=10,
        q=keywords
    )
    response = yt_request.execute()
    response_list = []
    for keyword in keywords.split(" "):
        pass
    for proposition in response['items']:
        try:
            prop = {'name': proposition['snippet']['title'],
                    'channel': proposition['snippet']['channelTitle'],
                    'id': proposition['id']['videoId'],
                    'thumbnail': proposition['snippet']['thumbnails']['medium']['url']}
            response_list.append(prop)
        except KeyError:
            pass
    return render(request, 'music_crawler/index.html', {'response_list': response_list})

def register_song(request):
    if request.method == "POST":
        response = {"status": "Downloading",
                    "error": False}
        try:
            music_tags = download_from_youtube(request.POST['id'])
            music_artist = Artist.objects.get_or_create(name=music_tags['artist'])
            new_music = Music.objects.create(
                title=music_tags['title'],
                duration=music_tags['duration'],
                artist=music_artist[0],
                cover=request.POST['thumbnail']
            )
            new_music.get_music_from_file()
            new_music.set_mp3_tags()
            response['status'] = 'Téléchargement effectué'

        except DownloadError as err:
            response['status'] = str(err) + " -- Vous pouvez réessayer"
            response['error'] = True
        return JsonResponse(response)
