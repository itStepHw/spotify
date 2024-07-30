from django.urls import path
from .views import *

from django.views.generic import TemplateView

urlpatterns = [
    path('', CategoryView.as_view(), name='category_view'),
    path('genre/<int:pk>', OneCategoryView.as_view(), name='genre_music'),
    path('music/<int:pk>', MusicDetail.as_view(), name='music_detail'),
    path('history/', HistoryView.as_view(), name='history'),
    path('upload_music/', UploadMusicView.as_view(), name='upload_music'),
    path('playlists/', PlaylistView.as_view(), name='playlist'),
    path('playlists/<int:pk>', PlaylistViewDetailView.as_view(), name='playlist_detail'),
    path('error/', TemplateView.as_view(template_name='spotify/error.html'), name='error'),
    path('playlist/<int:pk>/delete', PlaylistDeleteView.as_view(), name='delete_playlist'),
    path('albums/', AlbumsListView.as_view(), name='album_view'),
    path('album_detail/<int:pk>', AlbumDetailView.as_view(), name='album_detail_view')

]