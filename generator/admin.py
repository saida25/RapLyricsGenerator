from django.contrib import admin
from .models import Artist, Lyrics, GeneratedLyrics

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Lyrics)
class LyricsAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'created_at']
    list_filter = ['artist', 'created_at']
    search_fields = ['title', 'lyrics']

@admin.register(GeneratedLyrics)
class GeneratedLyricsAdmin(admin.ModelAdmin):
    list_display = ['prompt', 'artist_style', 'created_at']
    list_filter = ['artist_style', 'created_at']
    readonly_fields = ['created_at']