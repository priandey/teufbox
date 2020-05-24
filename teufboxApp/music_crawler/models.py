from django.db import models
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.conf.global_settings import MEDIA_ROOT
from mutagen.easyid3 import EasyID3

import os

class Music(models.Model):
    title = models.CharField(max_length=255)
    duration = models.DurationField(null=True)
    cover = models.URLField(true=True)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE, related_name='songs', null=True)
    album = models.CharField(max_length=255, default="None", null=True)
    yt_id = models.CharField(max_length=100, unique=True)
    media = models.FileField(upload_to='music/', null=True)

    def __str__(self):
        return self.title

    def get_music_from_file(self):
        """
        Retrieve music from its downloaded location to store it in media root, then get rid of original file
        """
        path_to_media_file = os.path.join(MEDIA_ROOT, f'{self.title}.mp3')
        with open(os.path.join(os.getcwd(), f'music_crawler/music/{self.yt_id}.mp3'), "rb") as fh:
            with ContentFile(fh.read()) as file_content:
                self.media.save(path_to_media_file, file_content)
                self.save()
        print(self.media.path)
        os.remove(fh.name)
        del fh

    def set_mp3_tags(self):
        audio = EasyID3("./media/music/" + self.media.path.split("/")[-1])
        audio.save()
        return True

class Artist(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class DownloadCount(models.Model):
    count = models.IntegerField(default=1)

class CachedMusic(models.Model):
    title = models.CharField(max_length=255)
    yt_id = models.CharField(max_length=100, null=True, unique=True)
    thumbnail = models.URLField(blank=True)
    is_downloading = models.BooleanField(default=False)

    @property
    def is_local(self):
        if len(Music.objects.filter(yt_id=self.yt_id)) > 0:
            return True
        else:
            return False
