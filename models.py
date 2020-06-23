from __future__ import unicode_literals
import os
import youtube_dl
import pprint

class ExternalMusic():
    def __init__(self, name, channel, id):
        self.name = name
        self.channel = channel
        self.id = id
        self.yt_url = "https://www.youtube.com/watch?v="

        self.complete_url()

    def __repr__(self):
        return f'{self.name}, from {self.channel}'

    def complete_url(self):
        self.yt_url += self.id

    def download(self):
        def my_hook(d):
            if d['status'] == 'finished':
                print('Done downloading, now converting ...')

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'music/pending.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
                {'key': 'FFmpegMetadata'}],
            'progress_hooks': [my_hook],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            youtube = ydl.download([self.yt_url])
