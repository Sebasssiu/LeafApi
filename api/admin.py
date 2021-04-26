from django.contrib import admin
from .models import *


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'artist_name', 'is_artist', 'is_admin', 'is_staff']


@admin.register(Listen)
class ListenAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'song', 'date']


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(PlayList)
class PlayListAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'name']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'genre', 'album_id']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'task_1', 'task_2', 'task_3', 'task_4', 'task_5', 'task_6', 'task_7', 'task_8']


admin.site.register(Premium)
