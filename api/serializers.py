from rest_framework import serializers
from .models import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class PremiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Premium
        fields = ('suscription', 'User')


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'name', 'artist_id', 'release_date', 'user')


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'name', 'genre', 'album_id', 'is_active', 'user', 'listen')

class GenreSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True)
    class Meta:
        model = Genre
        fields = ('id', 'name', 'songs')


class ListenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listen
        fields = ('id', 'listener', 'date')
