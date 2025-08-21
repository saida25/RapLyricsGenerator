import os
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, TrainingArguments, Trainer
from transformers import DataCollatorForLanguageModeling
from datasets import Dataset

def preprocess_function(examples, tokenizer, max_length):
    """Tokenize the texts"""
    return tokenizer(
        examples['text'], 
        truncation=True, 
        padding='max_length', 
        max_length=max_length,
        return_special_tokens_mask=True
    )

class RapLyricsTrainer:
    def __init__(self, model_name="gpt2"):
        self.model_name = model_name
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        
    def train(self, dataset, output_dir="./models", epochs=3, batch_size=4):
        """Fine-tune the model on the provided dataset"""
        # Data collator for language modeling
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False  # We're doing causal LM, not masked LM
        )
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            overwrite_output_dir=True,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            save_steps=500,
            save_total_limit=2,
            prediction_loss_only=True,
            logging_steps=100,
            logging_dir='./logs',
        )
        
        # Initialize Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=dataset,
        )
        
        # Train the model
        trainer.train()
        
        # Save the model
        trainer.save_model()
        self.tokenizer.save_pretrained(output_dir)
        
        return trainer
    
    def generate_lyrics(self, prompt, max_length=200, temperature=0.9, top_k=50, top_p=0.95):
        """Generate lyrics based on a prompt"""
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                temperature=temperature,
                top_k=top_k,
                top_p=top_p,
                repetition_penalty=1.2,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text