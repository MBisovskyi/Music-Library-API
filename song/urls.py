from django.urls import path
from . import views

urlpatterns = [
    path('', views.songs_list),
    path('<int:song_id>/', views.song_detail),
]