import os
import pandas as pd
from datasets import Dataset
from .model_trainer import preprocess_function

class DataProcessor:
    def __init__(self, data_dir="data/raw"):
        self.data_dir = data_dir
        
    def load_lyrics_from_db(self, artist_id=None):
        """Load lyrics from database and prepare for training"""
        from ..models import Lyrics, Artist
        
        if artist_id:
            lyrics_objs = Lyrics.objects.filter(artist_id=artist_id)
        else:
            lyrics_objs = Lyrics.objects.all()
            
        data = []
        for lyric in lyrics_objs:
            data.append({
                'artist': lyric.artist.name,
                'title': lyric.title,
                'lyrics': lyric.lyrics
            })
            
        return pd.DataFrame(data)
    
    def prepare_dataset(self, df, tokenizer, max_length=512):
        """Prepare dataset for training"""
        # Combine artist and lyrics for better context
        texts = []
        for _, row in df.iterrows():
            text = f"{row['artist']}: {row['lyrics']}"
            texts.append(text)
        
        # Create HuggingFace dataset
        dataset = Dataset.from_dict({'text': texts})
        
        # Tokenize
        tokenized_dataset = dataset.map(
            lambda examples: preprocess_function(examples, tokenizer, max_length),
            batched=True,
            remove_columns=dataset.column_names
        )
        
        return tokenized_dataset