from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


class Music(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='music/')
    image = models.ImageField(upload_to='images/')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, related_name='musics')
    genres = models.ManyToManyField(Genre, related_name='musics')
    likes = models.ManyToManyField('MusicLikes', related_name='liked_music', null=True, blank=True)
    history = models.ManyToManyField(User, related_name='music_history', through='History', blank=True)

    def __str__(self):
        return self.name


class MusicGenre(models.Model):
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    is_public = models.BooleanField(default=False)
    musics = models.ManyToManyField(Music, related_name='playlist')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class PlaylistMusic(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)


class History(models.Model):
    music = models.ForeignKey(Music, related_name='user_history_music', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listened_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.music.name}'


class MusicLikes(models.Model):
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



