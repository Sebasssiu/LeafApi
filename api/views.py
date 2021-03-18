from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import *
from django.db.models import Count
from datetime import datetime
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
