from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import *
from datetime import datetime, timedelta
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.db.models import Count
import datetime
from operator import itemgetter
from collections import defaultdict
from rest_framework.authtoken.views import ObtainAuthToken
from django.db import connection


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
            'artist_name': user.artist_name,
            'isPremium': user.is_staff,
            'isArtist': user.is_artist,
            'isAdmin': user.is_admin
        }
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def becomeArtist(self, request):
        token = Token.objects.get(key=request.data['token'])
        user = User.objects.get(id=token.user_id)
        user.artist_name = request.data['artist_name']
        user.is_artist = True
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
        Premium.objects.create(suscription_date=datetime.datetime.today().strftime('%Y-%m-%d'), users=user)
        return Response({'response': 'Successfull'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def lastsuscriptions(self, request):
        factual = datetime.datetime.today()
        semestreanterior = datetime.datetime.today() - timedelta(weeks=24)
        queryset = self.get_queryset().filter(suscription_date__range=[semestreanterior, factual])
        return Response(len(queryset))


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
        queryset = self.get_queryset().filter(release_date__range=[semanapasada, factual]).order_by('-release_date')
        serializer = ALbumDateSerializer(queryset, many=True)
        return Response(serializer.data)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class ListenViewSet(viewsets.ModelViewSet):
    queryset = Listen.objects.all()
    serializer_class = ListenSerializer

    @action(detail=False, methods=['GET'])
    def getingpopular(self, request):
        factual = datetime.datetime.today()
        hacemeses = datetime.datetime.today() - timedelta(weeks=12)
        queryset = self.get_queryset().filter(date__range=[hacemeses, factual])
        query = queryset.values('song').annotate(total=Count('song')).order_by('total')
        querylist = list(query)
        for i in querylist:
            temp_id = i['song']
            i['song'] = Song.objects.get(id=temp_id).user.username
        result = defaultdict(int)
        for d in querylist:
            result[d['song']] += int(d['total'])
        result = sorted(result.items(), key=lambda k_v: k_v[1], reverse=True)
        return Response(result)


    @action(detail=False, methods=['GET'])
    def mostactive(self, request):
        queryset = self.get_queryset().values('user').annotate(total=Count('user')).order_by('total')
        querylist = list(queryset)
        for i in querylist:
            temp_id = i['user']
            i['user'] = User.objects.get(id=temp_id).username
        querylist.sort(key=itemgetter('total'), reverse=True)
        finalquery = []
        for i in range (3):
            finalquery.append(querylist[i])
        return Response(finalquery)

    @action(detail=False, methods=['GET'])
    def populargenres(self, request):
        queryset = self.get_queryset().values('song').annotate(total=Count('song')).order_by('total')
        querylist = list(queryset)
        for i in querylist:
            temp_id = i['song']
            i['song'] = Song.objects.get(id=temp_id).genre.name
        result = defaultdict(int)
        for d in querylist:
            result[d['song']] += int(d['total'])
        result = sorted(result.items(), key=lambda k_v: k_v[1], reverse=True)
        finalresult = []
        for i in range(3):
            finalresult.append(result[i])

        return Response(finalresult)


class AllSongViewSet(viewsets.ModelViewSet):
  queryset = Song.objects.all()
  serializer_class = AllSongSerializer
  filter_backends = [SearchFilter]
  search_fields = ['name']

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
      song.link = request.data['data']['link']
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

    @action(detail=False, methods=['GET'])
    def popularartists(self, request):
        queryset = self.get_queryset().values('user').annotate(total=Count('user')).order_by('total')
        querylist = list(queryset)
        for i in querylist:
            temp_id = i['user']
            i['user'] = User.objects.get(id=temp_id).username
        querylist.sort(key=itemgetter('total'), reverse=True)
        finalquery = []
        for i in range(3):
            finalquery.append(querylist[i])
        return Response(finalquery)


class PlayListViewSet(viewsets.ModelViewSet):
    queryset = PlayList.objects.all()
    serializer_class = PlayListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['owner__id']

    @action(detail=False, methods=['POST'])
    def addSongToPlaylist(self, request):
      raw_query = f"INSERT INTO api_song_playlists (song_id, playlist_id) VALUES ({request.data['song_id']}, {request.data['playlist_id']})"
      cursor = connection.cursor()
      cursor.execute(raw_query)
      return Response({'response': 'Successfully'})

    @action(detail=False, methods=['POST'])
    def updateplaylist(self, request):
        token = Token.objects.get(key=request.data['token'])
        idd = request.data['id']
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


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk
        })