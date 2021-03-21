from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import *
from datetime import datetime
from django.core import serializers
from django.http import HttpResponse
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['POST'])
    def userData(self, request):
        token = Token.objects.get(key=request.data['token'])
        user = User.objects.get(id=token.user_id)
        response = {
            'username': user.username,
            'isPremium': user.is_staff,
            'isArtist': user.is_artist,
            'isAdmin': user.is_admin
        }
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def becomeArtist(self, request):
        token = Token.objects.get(key=request.data['token'])
        user = User.objects.get(id=token.user_id)
        user.is_artist = request.data['isArtist']
        user.artist_name = request.data['artist_name']
        user.save()
        return Response({'response': 'Successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def artistid(self, request):
        user = User.objects.get(id=request.data['id'])
        return Response({'name': user.artist_name}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def artists(self, request):
        queryset = self.get_queryset().filter(is_artist=True)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class PremiumViewSet(viewsets.ModelViewSet):
    queryset = Premium.objects.all()
    serializer_class = PremiumSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    @action(detail=False, methods=['POST'])
    def premiumPay(self, request):
        token = Token.objects.get(key=request.data['token'])
        user = User.objects.get(id=token.user_id)
        user.is_staff = True
        user.save()
        Premium.objects.create(User=user, suscription_date=datetime.today().strftime('%Y-%m-%d'))
        return Response({'response': 'Successfull'}, status=status.HTTP_200_OK)


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    @action(detail=False, methods=['POST'])
    def updatealbum(self, request):
        if request.data['delete'] == "song":
            print("holaa")
            Song.objects.get(id=request.data['song_id']).delete()
            print("holaasssssssss")
        elif request.data['delete'] == "artist":
            User.objects.get(id=request.data['artist_id']).delete()
        elif request.data['delete'] == "album":
            Album.objects.get(id=request.data['id']).delete()
        else:
            album = Album.objects.get(id=request.data['id'])
            album.name = request.data['album']
            album.save()
            song = Song.objects.get(id=request.data['song_id'])
            song.name = request.data['song']
            song.is_active = request.data['isSong']
            song.save()
            user = User.objects.get(id=request.data['artist_id'])
            user.artist_name = request.data['artist']
            user.save()
        return Response({'response': 'Successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def useralbum(self, request):
        token = Token.objects.get(key=request.data['token'])
        user = User.objects.get(id=token.user_id)
        queryset = self.get_queryset().filter(user=user.id)
        serializer = AlbumSerializer(queryset, many=True)
        return Response(serializer.data)


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

    @action(detail=False, methods=['POST'])
    def validation(self, request):
        token = Token.objects.get(key=request.data['token'])
        user = User.objects.get(id=token.user_id)
        if user.is_staff:
            return Response({'alert': 'Successfull'}, status=status.HTTP_200_OK)
        else:
            if request.data['song'] != "":
                count = Listen.objects.filter(date=datetime.today().strftime('%Y-%m-%d'), user=user.id)
                if len(count) < 3:
                    song = Song.objects.get(id=request.data['song'])
                    Listen.objects.create(user=user, song=song, date=datetime.today().strftime('%Y-%m-%d'))
                    return Response({'alert': 'Successfull'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'ERROR'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def addsong(self, request):
        print(request.data['song_id'])
        song = Song.objects.get(id=request.data['song_id'])
        print(song.playlists)
        return Response('successfull', status=status.HTTP_200_OK)


class PlayListViewSet(viewsets.ModelViewSet):
    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['owner__id']

    @action(detail=False, methods=['POST'])
    def createplaylist(self, request):
        token = Token.objects.get(key=request.data['token'])
        user = User.objects.get(id=token.user_id)
        pname = request.data['name']
        print(pname)
        PlayList.objects.create(owner=user, name=pname)
        response = {'message': 'playlist created'}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def userPlaylist(self, request):
        token = Token.objects.get(key=request.data['token'])
        user = User.objects.get(id=token.user_id)
        queryset = self.get_queryset().filter(owner=user.id)
        serializer = PlayListSerializer(queryset, many=True)
        return Response(serializer.data)
