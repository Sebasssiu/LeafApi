from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('premium', PremiumViewSet)
router.register('genres', GenreViewSet)
router.register('albums', AlbumViewSet)
router.register('listen', ListenViewSet)
router.register('songs', SongViewSet)
router.register('playlists', PlayListViewSet)
router.register('allSongs', AllSongViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(r'api-token-auth/', CustomAuthToken.as_view())
]
