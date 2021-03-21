from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class Users(AbstractUser):
    artist_name = models.CharField(max_length=32, blank=True, default='')
    is_artist = models.BooleanField(default=False, blank=False)
    is_admin = models.BooleanField(default=False, blank=False)
    is_staff = models.BooleanField(default=False, blank=False)

User = get_user_model()

class Premium(models.Model):
    suscription_date = models.DateField(blank=False)
    User = models.ForeignKey(User, on_delete=models.CASCADE)


class Album(models.Model):
    name = models.CharField(max_length=32, blank=False)
    artist_id = models.CharField(max_length=32, blank=False)
    release_date = models.DateField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Genre(models.Model):
    name = models.CharField(max_length=32, blank=False)

class PlayList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    name = models.CharField(max_length=30, blank=False)

class Song(models.Model):
    name = models.CharField(max_length=32, blank=False)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='songs')
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='almbum_songs')
    is_active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.CharField(max_length=300, blank=False, default="null")
    playlists = models.ManyToManyField(PlayList, related_name='songs')

class Listen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    date = models.DateField(blank=False)


