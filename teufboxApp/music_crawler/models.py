from django.db import models
from django.core.files.base import ContentFile
from django.conf.global_settings import MEDIA_ROOT

import os

class Music(models.Model):
    title = models.CharField(max_length=255)
    duration = models.DurationField(null=True)
    cover = models.URLField(blank=True)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE, related_name='songs', null=True)
    media = models.FileField(upload_to='music/', blank=True)  # Idem

    def __str__(self):
        return self.title

    def get_music_from_file(self):
        with open(os.path.join(os.getcwd(), 'music_crawler/music/pending.mp3'), "rb") as fh:
            with ContentFile(fh.read()) as file_content:
                self.media.save(os.path.join(MEDIA_ROOT, f'{self.title}.mp3'), file_content)
                self.save()
        os.remove(fh.name)
        del fh

class Artist(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name