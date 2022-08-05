from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SongSerializer
from .models import Song
from rest_framework import status

# Create your views here.
@api_view(['GET', 'POST'])
def songs_list(request):
    if request.method == 'GET':
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many = True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SongSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def song_detail(request, pk):
    song = get_object_or_404(Song, pk = pk)
    if request.method == 'GET':
        serializer = SongSerializer(song)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SongSerializer(song, data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        song.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'DELETE'])
def like_toggle(request, pk):
    song = get_object_or_404(Song, id = pk)
    if request.method == 'GET':
        serializer = SongSerializer(song)
        song.likes_quantity = str(song.likes_quantity + 1)
        song.likes_quantity = int(song.likes_quantity)
        new_song = song_dict(song)
        serializer = SongSerializer(song, data = new_song)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        likes_quantity_response = (f"Likes quantity: {song.likes_quantity}")
        return Response(likes_quantity_response, status = status.HTTP_202_ACCEPTED)
    elif request.method == 'DELETE':
        serializer = SongSerializer(song)
        if song.likes_quantity > 0:
            song.likes_quantity = str(song.likes_quantity - 1)
            song.likes_quantity = int(song.likes_quantity)
            new_song = song_dict(song)
        else:
            song.likes_quantity = '0'
            song.likes_quantity = int(song.likes_quantity)
            new_song = song_dict(song)
        serializer = SongSerializer(song, data = new_song)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        likes_quantity_response = (f"Likes quantity: {song.likes_quantity}")
        return Response(likes_quantity_response, status = status.HTTP_202_ACCEPTED)

def song_dict(song):
    new_song = {
        "title": song.title,
        "artist": song.artist,
        "album": song.album,
        "release_date": song.release_date,
        "genre": song.genre,
        "likes_quantity": song.likes_quantity,
    }
    return new_song