import subprocess
import youtube_dl
from tinytag import TinyTag
from datetime import timedelta
from .models import DownloadCount

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
    if download_count.count % 10 == 0:
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
    print(music_tags)
    tags = {
        'title': music_tags.title,
        'duration': timedelta(seconds=music_tags.duration),
        'artist': music_tags.artist
    }
    return tags