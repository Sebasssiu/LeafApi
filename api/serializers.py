from rest_framework import serializers
from .models import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()


class ListenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Listen
        fields = ('id', 'song', 'user', 'date')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'artist_name', 'is_artist', 'is_admin', 'is_staff', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True},
                        'artist_name': {'required': False},
                        'is_artist': {'required': False},
                        'is_admin': {'required': False},
                        'is_staff': {'required': False}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class PremiumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Premium
        fields = ('suscription_date', 'users')


class IsActiveListSerializer(serializers.ListSerializer):

  def to_representation(self, data):
    data = data.filter(is_active=True)
    return super().to_representation(data)

class SongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = ('id', 'name', 'genre', 'album_id', 'is_active', 'user', 'link')
        list_serializer_class = IsActiveListSerializer


class AllSongSerializer(serializers.ModelSerializer):
  class Meta:
    model = Song
    fields = ('id', 'name', 'genre', 'album_id', 'is_active', 'user', 'link')


class PlayListSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True)

    class Meta:
        model = PlayList
        fields = ('id', 'owner', 'name', 'songs')


class AlbumSerializer(serializers.ModelSerializer):
    almbum_songs = SongSerializer(many=True)

    class Meta:
        model = Album
        fields = ('id', 'name', 'release_date', 'user', 'almbum_songs')


class GenreSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True)

    class Meta:
        model = Genre
        fields = ('id', 'name', 'songs')


class ALbumDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('name', 'release_date')









