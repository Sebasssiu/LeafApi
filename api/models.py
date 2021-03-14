from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(models.Model):
    username = models.CharField(max_length=32, primary_key=True, blank=False)
    artist_name = models.CharField(max_length=32, blank=True)
    password = models.CharField(max_length=50, blank=False)
    is_artist = models.BooleanField(default=False, blank=False)
    is_admin = models.BooleanField(default=False, blank=False)
    is_staff = models.BooleanField(default=False, blank=False)


class Premium(models.Model):
    suscription_date = models.DateField(blank=False)
    User = models.ForeignKey(Users, on_delete=models.CASCADE)


class Album(models.Model):
    name = models.CharField(max_length=32, blank=False)
    artist_id = models.CharField(max_length=32, blank=False)
    release_date = models.DateField(blank=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)


class Genre(models.Model):
    name = models.CharField(max_length=32, blank=False)


class Listen(models.Model):
    listener = models.ManyToManyField('Users', through="Song")
    date = models.DateField(blank=False)


class Song(models.Model):
    name = models.CharField(max_length=32, blank=False)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    listen = models.ForeignKey('Listen', on_delete=models.CASCADE)

