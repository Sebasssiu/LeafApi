from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'artist_name', 'is_artist', 'is_admin', 'is_staff']


@admin.register(Listen)
class ListenAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'song', 'date']


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'artist_id']


@admin.register(PlayList)
class PlayListAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'name']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'genre', 'album_id']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Premium)
