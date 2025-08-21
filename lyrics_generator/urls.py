from django.contrib import admin
from django.urls import path
from generator import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('artists/', views.artist_list, name='artist_list'),
    path('artists/add/', views.add_artist, name='add_artist'),
    path('lyrics/', views.lyrics_list, name='lyrics_list'),
    path('lyrics/add/', views.add_lyrics, name='add_lyrics'),
    path('train/', views.train_model, name='train_model'),
    path('generate/', views.generate_lyrics, name='generate_lyrics'),
    path('generated/', views.generated_lyrics_list, name='generated_lyrics_list'),
]