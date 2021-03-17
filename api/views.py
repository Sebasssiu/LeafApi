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
from rest_framework.filters import SearchFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PremiumViewSet(viewsets.ModelViewSet):
    queryset = Premium.objects.all()
    serializer_class = PremiumSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class ListenViewSet(viewsets.ModelViewSet):
    queryset = Listen.objects.all()
    serializer_class = ListenSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    @action(detail=True, methods=['GET'])
    def song_info(self, request, pk=None):
        song = Song.objects.get(id=pk)
        song_name = song.name
        response = {'Song requested': song_name}
        return Response(response, status=status.HTTP_200_OK)

