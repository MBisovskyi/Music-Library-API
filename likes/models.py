from django.db import models
from song.models import Song

# Create your models here.
class SongLike(models.Model):
    song = models.ForeignKey(Song, on_delete = models.CASCADE)