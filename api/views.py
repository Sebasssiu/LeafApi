from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import *
from datetime import datetime, timedelta
from django.core import serializers
from django.http import HttpResponse
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
import datetime
from django.db.models import Count


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

    @action(detail=False, methods=['POST'])
    def modifyUser(self, request):
      if request.data['data']['delete']:
        User.objects.get(id=request.data['item']['id']).delete()
        return Response({'response': 'Successfully'}, status=status.HTTP_200_OK)
      user = User.objects.get(id=request.data['item']['id'])
      user.artist_name = request.data['data']['name']
      user.save()
      return Response({'response': 'Successfully'}, status=status.HTTP_200_OK)

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
        Premium.objects.create(user=user, suscription_date=datetime.today().strftime('%Y-%m-%d'))
        return Response({'response': 'Successfull'}, status=status.HTTP_200_OK)


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    @action(detail=False, methods=['POST'])
    def modifyAlbum(self, request):
      if request.data['data']['delete']:
        Album.objects.get(id=request.data['item']['id']).delete()
        return Response({'response': 'Successfully'}, status=status.HTTP_200_OK)
      album = Album.objects.get(id=request.data['item']['id'])
      album.name = request.data['data']['name']
      album.save()
      return Response({'response': 'Successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def useralbum(self, request):
        token = Token.objects.get(key=request.data['token'])
        user = User.objects.get(id=token.user_id)
        queryset = self.get_queryset().filter(user=user.id)
        serializer = AlbumSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def createalbum(self, request):
        token = Token.objects.get(key=request.data['token'])
        user = User.objects.get(id=token.user_id)
        aname = request.data['name']
        release = datetime.datetime.now()
        Album.objects.create(name=aname, artist_id=user, release_date=release, user=user)
        response = {'message': 'album created'}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def recentalbums(self, request):
        factual = datetime.datetime.today()
        semanapasada = datetime.datetime.today() - timedelta(7)
        queryset = self.get_queryset().filter(release_date__range=[semanapasada, factual])
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
    @action (detail=False, methods=['GET'])
    def artistpopularity(self, request):
        factual = datetime.datetime.today()
        lastmonths = factual - datetime.timedelta(weeks=12)
        queryset = self.get_queryset().filter(date__range=[lastmonths, factual])
        #b = queryset.annotate()
        serializer = ListenSerializer(queryset, many=True)
        return Response(serializer.data)


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    @action(detail=False, methods=['POST'])
    def modifySong(self, request):
      if request.data['data']['delete']:
        Song.objects.get(id=request.data['item']['id']).delete()
        return Response({'response': 'Successfully'}, status=status.HTTP_200_OK)
      song = Song.objects.get(id=request.data['item']['id'])
      song.name = request.data['data']['name']
      song.is_active = request.data['data']['isActive']
      song.save()
      return Response({'response': 'Successfully'}, status=status.HTTP_200_OK)

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
            songid = request.data['song']
            if Song.objects.filter(id=songid).exists():
                song = Song.objects.get(id=request.data['song'])
                Listen.objects.create(user=user, song=song, date=datetime.datetime.today())
                return Response({'alert': 'Successfull'}, status=status.HTTP_200_OK)
            else:
                return Response({'alert': 'ERROR'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            songid = request.data['song']
            if Song.objects.filter(id=songid).exists():
                if songid != "":
                    count = Listen.objects.filter(date=datetime.datetime.now(), user=user.id)
                    if len(count) < 3:
                        song = Song.objects.get(id=request.data['song'])
                        Listen.objects.create(user=user, song=song, date=datetime.datetime.today())
                        return Response({'alert': 'Successfull'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'error': 'ERROR'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'alert': 'ERROR'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def addsong(self, request):
        print(request.data['song_id'])
        song = Song.objects.get(id=request.data['song_id'])
        print(song.playlists)
        return Response('successfull', status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def createsong(self, request):
        token = Token.objects.get(key=request.data['token'])
        user = User.objects.get(id=token.user_id)
        songname = request.data['name']
        songgenre = request.data['genre']
        genre = Genre.objects.filter(name=songgenre)
        songlink = request.data['link']
        songdate = request.data['date']
        songalbum = request.data['album']
        album = Album.objects.filter(id=songalbum)
        Song.objects.create(name=songname, genre=genre.first(), album_id=album.first(), is_active=True, user=user, link=songlink)
        response = {'message': 'song created'}
        return Response(response, status=status.HTTP_200_OK)


class PlayListViewSet(viewsets.ModelViewSet):
    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['owner__id']

    @action(detail=False, methods=['POST'])
    def updateplaylist(self, request):
        token = Token.objects.get(key=request.data['token'])
        user = User.objects.get(id=token.user_id)
        idd = request.data['id']
        #pname = request.data['name']
        #pl = PlayList.objects.filter(name=pname).first()
        items = Song.objects.filter(id=idd)
        print(items.first().playlists)
        response = {'message': 'song added'}
        return Response(response, status=status.HTTP_200_OK)

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
