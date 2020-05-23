import os
import json

import googleapiclient.discovery
import googleapiclient.errors

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Music, Artist, CachedMusic
from .utils import download_one_song

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
                    'thumbnail': proposition['snippet']['thumbnails']['default']['url']}
            response_list.append(prop)
        except KeyError:
            pass
    return JsonResponse(response_list, safe=False)

@csrf_exempt
def downloader(request):
    """
    The downloader is an interface between front-end query for downloading and back-end downloading processes

    :param request:

        request.body should be json.stringify type and contain at least 2 arguments :
            multiple : Boolean | Represent if the downloader contain one or more songs to download

            if multiple is true :
                download_queue : List of json : { yt_id : string | id of youtube video
                                                  thumbnail: string | url of thumbnail picture }
            if multiple is false :
                yt_id : string | id of youtube video
                thumbnail: string | url of thumbnail picture
    :return:
    """
    if request.method == "POST":
        response = {"status": "Downloading",
                    "error": False}
        raw_data = request.body.decode('utf-8')
        data = json.loads(raw_data)
        if not data["multiple"]:
            set_to_downloading(data["music"])
            download_one_song(data['music'], response)
        elif data["multiple"]:
            for music in data["download_queue"]:  # Setting all music flag to "downloading"
                set_to_downloading(music)
            for music in data["download_queue"]:
                download_one_song(music, response)
        else:
            response = "Wrong instructions"
        return JsonResponse(response)


def set_to_downloading(music):
    update_status = CachedMusic.objects.get(yt_id=music['id'])
    update_status.is_downloading = True
    update_status.save()


@csrf_exempt
def music_cache(request):
    if request.method == "GET":
        if request.GET['music'] == 'all':
            music_cached = CachedMusic.objects.all()
            serialized_cache = []
            if music_cached:
                for music in music_cached:
                    serialized_cache.append({
                        'title': music.title,
                        'yt_id': music.yt_id,
                        'thumbnail': music.thumbnail,
                        'is_local': music.is_local,
                        'is_downloading': music.is_downloading
                    })

            return JsonResponse(serialized_cache, safe=False)

    if request.method == "POST":
        add_to_cache = CachedMusic.objects.create(
                title=request.POST['title'],
                yt_id=request.POST['id'],
                thumbnail=request.POST['thumbnail']
        )
        add_to_cache.save()
        return JsonResponse({"status" : "Added music to cache"})

    if request.method == "DELETE":
        if request.GET['id'] == "all":
            CachedMusic.objects.all().delete()
        else:
            CachedMusic.objects.filter(yt_id=request.GET['id'])[0].delete()

        return JsonResponse({"status": "Deleted music from cache"})
