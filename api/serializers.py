from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'username', 'artist_name', 'password', 'is_artist', 'is_admin','is_staff')


class PremiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Premium
        fields = ('suscription', 'User')


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'name', 'artist_id', 'release_date', 'user')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class ListenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listen
        fields = ('id', 'listener', 'date')


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ('id', 'name', 'genre', 'album_id', 'is_active', 'user', 'listen')
