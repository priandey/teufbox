import subprocess
import pprint

from datetime import timedelta

import youtube_dl

from youtube_dl.utils import DownloadError

def download_from_youtube(yt_id):
    """
    Download a youtube video in a directory.
    :param yt_id : Youtube id of the video you need to download
    :return :  Return a serie of Tags in order to
    """
    download_count = DownloadCount.objects.get_or_create(pk=1)[0]
    download_count.count += 1
    download_count.save()
    print("Nombre de download = " + str(download_count.count))

    if download_count.count % 10 == 0:  # Empty cache directory frequently, as it caused errors in the past
        subprocess.run(['youtube-dl', '--rm-cache-dir'])

    def my_hook(d):
        if d['status'] == 'downloading':
            pass
        if d['status'] == 'finished':
            pass
        if d['status'] == 'error':
            pass

    yt_url = f'https://www.youtube.com/watch?v={yt_id}'

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'music_crawler/music/{yt_id}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
            {'key': 'FFmpegMetadata'}],
        'progress_hooks': [my_hook],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])

    music_tags = TinyTag.get(f'music_crawler/music/{yt_id}.mp3')
    tags = {
        'title': music_tags.title,
        'duration': timedelta(seconds=music_tags.duration),
        'artist': music_tags.artist,
        'album': music_tags.album
    }
    return tags

def download_one_song(music, response):
    try:
        music_tags = download_from_youtube(music['id'])
        music_artist = Artist.objects.get_or_create(name=music_tags['artist'])
        new_music = Music.objects.create(
            title=music_tags['title'],
            duration=music_tags['duration'],
            artist=music_artist[0],
            album=music_tags['album'],
            yt_id=music['id'],
            cover=music['thumbnail']
        )
        new_music.get_music_from_file()
        new_music.set_mp3_tags()
        response['status'] = 'Téléchargement effectué'

    except DownloadError as err:
        response['status'] = str(err) + " -- Vous pouvez réessayer"
        response['error'] = True

def search_song(request):
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.getenv("GOOGLE_KEY")
    youtube = googleapiclient.discovery.build(api_service_name,
                                              api_version,
                                              developerKey=DEVELOPER_KEY)
    keywords = request.GET['keywords']
    yt_request = youtube.search().list(
        part="snippet",
        maxResults=10,
        q=keywords
    )
    response = yt_request.execute()
    response_list = []

    for proposition in response['items']:
        try:
            prop = {'name': proposition['snippet']['title'],
                    'channel': proposition['snippet']['channelTitle'],
                    'id': proposition['id']['videoId'],
                    'thumbnail': proposition['snippet']['thumbnails']['default']['url'],
                    'is_local': False}
            search_db = Music.objects.filter(yt_id=prop['id'])

            if search_db:
                prop['name'] = search_db[0].title
                prop['channel'] = "TeufBox"
                prop['thumbnail'] = search_db[0].cover
                prop['is_local'] = True

            response_list.append(prop)
        except KeyError:
            pass

    return JsonResponse(response_list, safe=False)