import youtube_dl
from tinytag import TinyTag
from datetime import timedelta

def download_from_youtube(yt_id):
    """
    Download a youtube video in a directory.
    :param yt_id : Youtube id of the video you need to download
    :return :  Return a serie of Tags in order to
    """
    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    yt_url = f'https://www.youtube.com/watch?v={yt_id}'

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music_crawler/music/pending.%(ext)s',
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

    music_tags = TinyTag.get('music_crawler/music/pending.mp3')
    print(music_tags)
    tags = {
        'title': music_tags.title,
        'duration': timedelta(seconds=music_tags.duration),
        'artist': music_tags.artist
    }
    return tags