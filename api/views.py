from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
# Create your views here.
from .serializers import *
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PremiumViewSet(viewsets.ModelViewSet):
    queryset = Premium.objects.all()
    serializer_class = PremiumSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ListenViewSet(viewsets.ModelViewSet):
    queryset = Listen.objects.all()
    serializer_class = ListenSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    @action(detail=True, methods=['GET'])
    def song_info(self, request, pk=None):
        song = Song.objects.get(id=pk)
        song_name = song.name
        response = {'Song requested': song_name}
        return Response(response, status=status.HTTP_200_OK)

