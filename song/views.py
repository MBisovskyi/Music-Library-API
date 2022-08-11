from functools import partial
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


@api_view(['PATCH', 'DELETE'])
def like_toggle(request, pk):
    song = get_object_or_404(Song, id = pk)
    if request.method == 'PATCH':
        song.likes_quantity += 1
        serializer = SongSerializer(song, data = request.data, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        likes_quantity_response = (f"Likes quantity: {song.likes_quantity}")
        return Response(likes_quantity_response, status = status.HTTP_202_ACCEPTED)
    elif request.method == 'DELETE':
        if song.likes_quantity > 0:
            song.likes_quantity -= 1
        else:
            song.likes_quantity = 0
        serializer = SongSerializer(song, data = request.data, partial = True)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        likes_quantity_response = (f"Likes quantity: {song.likes_quantity}")
        return Response(likes_quantity_response, status = status.HTTP_202_ACCEPTED)

