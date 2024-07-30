from django import forms
from .models import *


class AddMusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = 'name', 'file', 'image', 'album', 'genres'



class PlaylistForm(forms.ModelForm):

    class Meta:
        model = Playlist
        fields = 'name', 'is_public'
