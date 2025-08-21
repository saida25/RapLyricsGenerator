from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
import os
import json

from .models import Artist, Lyrics, GeneratedLyrics
from .forms import ArtistForm, LyricsForm, GenerateForm
from .utils.data_processor import DataProcessor
from .utils.model_trainer import RapLyricsTrainer

def index(request):
    return render(request, 'index.html')

def artist_list(request):
    artists = Artist.objects.all()
    return render(request, 'artists.html', {'artists': artists})

def add_artist(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artist added successfully!')
            return redirect('artist_list')
    else:
        form = ArtistForm()
    return render(request, 'add_artist.html', {'form': form})

def add_lyrics(request):
    if request.method == 'POST':
        form = LyricsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lyrics added successfully!')
            return redirect('lyrics_list')
    else:
        form = LyricsForm()
    return render(request, 'add_lyrics.html', {'form': form})

def lyrics_list(request):
    lyrics = Lyrics.objects.all().select_related('artist')
    return render(request, 'lyrics_list.html', {'lyrics': lyrics})

def train_model(request):
    if request.method == 'POST':
        artist_id = request.POST.get('artist')
        
        # Initialize data processor and trainer
        processor = DataProcessor()
        trainer = RapLyricsTrainer()
        
        # Load data
        df = processor.load_lyrics_from_db(artist_id if artist_id != 'all' else None)
        
        if len(df) < 5:
            messages.error(request, 'Not enough lyrics data for training. Please add more lyrics.')
            return redirect('train_model')
        
        # Prepare dataset
        dataset = processor.prepare_dataset(df, trainer.tokenizer)
        
        # Train model
        output_dir = os.path.join(settings.BASE_DIR, 'models', f'artist_{artist_id}' if artist_id != 'all' else 'all_artists')
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            trainer.train(dataset, output_dir=output_dir, epochs=3)
            messages.success(request, 'Model trained successfully!')
        except Exception as e:
            messages.error(request, f'Error training model: {str(e)}')
        
        return redirect('generate_lyrics')
    
    artists = Artist.objects.all()
    return render(request, 'train.html', {'artists': artists})

def generate_lyrics(request):
    if request.method == 'POST':
        form = GenerateForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            artist_style = form.cleaned_data['artist_style']
            length = int(request.POST.get('length', 200))
            
            # Load appropriate model
            model_dir = os.path.join(
                settings.BASE_DIR, 
                'models', 
                f'artist_{artist_style.id}' if artist_style else 'all_artists'
            )
            
            if not os.path.exists(model_dir):
                messages.error(request, 'No model found for this artist. Please train a model first.')
                return redirect('train_model')
            
            try:
                trainer = RapLyricsTrainer()
                trainer.tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
                trainer.model = GPT2LMHeadModel.from_pretrained(model_dir)
                
                # Generate lyrics
                generated = trainer.generate_lyrics(prompt, max_length=length)
                
                # Save generated lyrics
                gen_lyrics = GeneratedLyrics(
                    prompt=prompt,
                    lyrics=generated,
                    artist_style=artist_style
                )
                gen_lyrics.save()
                
                return render(request, 'generate_result.html', {
                    'generated_lyrics': generated,
                    'prompt': prompt
                })
                
            except Exception as e:
                messages.error(request, f'Error generating lyrics: {str(e)}')
                return redirect('generate_lyrics')
    else:
        form = GenerateForm()
    
    return render(request, 'generate.html', {'form': form})

def generated_lyrics_list(request):
    lyrics = GeneratedLyrics.objects.all().select_related('artist_style')
    return render(request, 'generated_list.html', {'lyrics': lyrics})