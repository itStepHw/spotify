from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from .models import *

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .form import *
from django.urls import reverse_lazy


#Миксины



@method_decorator(login_required(login_url='login'), name='dispatch')
class CategoryView(ListView):
    model = Genre
    template_name = 'spotify/index.html'
    context_object_name = 'genres'


@method_decorator(login_required(login_url='login'), name='dispatch')
class AlbumsListView(ListView):
    template_name = 'spotify/albums.html'
    model = Album
    context_object_name = 'albums'




@method_decorator(login_required(login_url='login'), name='dispatch')
class OneCategoryView(DetailView):
    model = Genre
    template_name = 'spotify/music.html'
    context_object_name = 'genres'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = context.get('genres')
        context['musics'] = genre.musics.all()
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class AlbumDetailView(DetailView):
    model = Album
    template_name = 'spotify/album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = context.get('album')
        context['musics'] = album.musics.all()
        return context




@method_decorator(login_required(login_url='login'), name='dispatch')
class MusicDetail(DetailView):
    model = Music
    template_name = 'spotify/one_music.html'
    context_object_name = 'music'

    def get(self, request, *args, **kwargs):
        History.objects.create(
            music=Music.objects.get(pk=self.kwargs['pk']),
            user=self.request.user
        )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        music = Music.objects.get(pk=self.kwargs['pk'])
        playlist = Playlist.objects.get(pk=self.request.POST['playlist'])
        playlist.musics.add(music)


        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        music = context.get('music')
        genres = music.genres.all()
        context['genre'] = genres
        context['genres_str'] = ', '.join(map(lambda genre: genre.name, genres))

        context['playlists'] = self.request.user.playlists.all()
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class HistoryView(ListView):
    model = History
    template_name = 'spotify/history.html'
    context_object_name = 'histories'
    paginate_by = 15

    def get_queryset(self):
        return History.objects.filter(user=self.request.user).order_by('-listened_at')


@method_decorator(login_required(login_url='login'), name='dispatch')
class UploadMusicView(CreateView):
    template_name = 'spotify/upload_music.html'
    model = Music
    form_class = AddMusicForm

    def form_valid(self, form):
        music = form.save(commit=False)
        music.author = self.request.user
        music.save()
        form.save_m2m()
        return redirect('category_view')


@method_decorator(login_required(login_url='login'), name='dispatch')
class PlaylistView(ListView):
    model = Playlist
    context_object_name = 'playlists'
    template_name = 'spotify/playlist.html'

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_playlists = []

        for playlist in context['playlists']:
            music = playlist.musics.all()

            new_playlist = {
                'id': playlist.id,
                'name': playlist.name,
                'musics': music,
                'created_at': playlist.created_at,
                'image': music[0].image if len(music) > 0 else 'images/default.jpg'
            }
            new_playlists.append(new_playlist)
        context['new_playlists'] = new_playlists
        context['form'] = PlaylistForm()
        return context

    def post(self, *args, **kwargs):
        form = PlaylistForm(self.request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = self.request.user
            playlist.save()
        return super().get(*args, **kwargs)


@method_decorator(login_required(login_url='login'), name='dispatch')
class PlaylistViewDetailView(DetailView):
    model = Playlist
    template_name = 'spotify/playlist_detail.html'
    context_object_name = 'playlist'

    def get(self, request, *args, **kwargs):

        playlist = Playlist.objects.get(pk=self.kwargs['pk'])

        if request.user.id != playlist.user.id:
            if not playlist.is_public:
                return redirect('error')

        return super().get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        playlist = Playlist.objects.get(pk=self.kwargs['pk'])

        if playlist.user != request.user:
            return redirect('error')

        music_id = self.request.POST['delete_button']

        music = Music.objects.get(pk=music_id)
        playlist.musics.remove(music)

        return super().get(request, *args, **kwargs)


@method_decorator(login_required(login_url='login'), name='dispatch')
class PlaylistDeleteView(DeleteView):
    template_name = 'spotify/delete_confirm.html'
    model = Playlist
    context_object_name = 'playlist'
    success_url = reverse_lazy('playlist')

    def post(self, request, *args, **kwargs):
        playlist = Playlist.objects.get(pk=self.kwargs['pk'])

        if playlist.user.id != request.user.id:
            return redirect('error')

        playlist.delete()
        return redirect("playlist")



