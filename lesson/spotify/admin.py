from django.contrib import admin
from .models import *


admin.site.register(
    [Genre,
     Album,
     Music,
     MusicGenre,
     Playlist,
     PlaylistMusic,
     History,
     MusicLikes
     ]
)
