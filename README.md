# Rap Lyrics Generator - Django Project

## Project Overview
This Django application fine-tunes a GPT-2 model on rap lyrics to generate new lyrics in the style of specific artists using HuggingFace Transformers.

## Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)

## Setup Instructions

### Step 1: Create and Activate Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Create Django Project
```bash
# Install Django
pip install Django

# Create project directory
mkdir rap_lyrics_generator
cd rap_lyrics_generator

# Create Django project
django-admin startproject lyrics_generator .

# Create main app
python manage.py startapp generator
```

### Step 3: Install Dependencies
Create a `requirements.txt` file with the content provided earlier, then install:
```bash
pip install -r requirements.txt
```

### Step 4: Configure Project Structure
Create the following directories inside your project:
```bash
mkdir -p utils data/raw data/processed static/css static/js templates
```

### Step 5: Update Settings
Add your app to `lyrics_generator/settings.py`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'generator',  # Add your app here
]
```

### Step 6: Create Models
Add the models from the provided code to `generator/models.py`

### Step 7: Create URLs
Create `generator/urls.py` and update the main `lyrics_generator/urls.py`:
```python
# lyrics_generator/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('generator.urls')),
]
```

### Step 8: Create Templates
Create the HTML templates in the `templates` directory as provided.

### Step 9: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 10: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 11: Run Development Server
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see your application.

## Project Structure
```
rap_lyrics_generator/
├── lyrics_generator/          # Django project folder
│   ├── __init__.py
│   ├── settings.py           # Project settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py
├── generator/                 # Main application
│   ├── __init__.py
│   ├── admin.py              # Admin configuration
│   ├── apps.py
│   ├── models.py             # Database models
│   ├── tests.py
│   ├── views.py              # Application views
│   ├── urls.py               # Application URLs
│   └── utils/                # Utility functions
│       ├── __init__.py
│       ├── data_processor.py # Data processing utilities
│       └── model_trainer.py  # Model training utilities
├── data/                     # Data directory
│   ├── raw/                  # Raw data files
│   └── processed/            # Processed data files
├── templates/                # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── generate.html
│   ├── train.html
│   └── lyrics_list.html
├── static/                   # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── manage.py                 # Django management script
└── requirements.txt          # Python dependencies
```

## Usage Workflow
1. Add artists through the admin interface or frontend
2. Add lyrics for those artists
3. Train the model on specific artists or all artists
4. Generate new lyrics using prompts and selected artist styles

## Additional Notes
- The application uses HuggingFace Transformers for the GPT-2 model
- Training requires sufficient lyrics data (recommended at least 20-30 songs per artist for good results)
- Model training can be computationally intensive - consider using GPU for faster training
