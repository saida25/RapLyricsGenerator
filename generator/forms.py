from django import forms
from .models import Artist, Lyrics, GeneratedLyrics

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'description']

class LyricsForm(forms.ModelForm):
    class Meta:
        model = Lyrics
        fields = ['artist', 'title', 'lyrics']

class GenerateForm(forms.ModelForm):
    prompt = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter a starting phrase for the lyrics...'}),
        required=True
    )
    artist_style = forms.ModelChoiceField(
        queryset=Artist.objects.all(),
        required=False,
        empty_label="Generic (no specific artist)"
    )
    length = forms.IntegerField(
        min_value=50,
        max_value=1000,
        initial=200,
        help_text="Number of characters to generate"
    )
    
    class Meta:
        model = GeneratedLyrics
        fields = ['prompt', 'artist_style']