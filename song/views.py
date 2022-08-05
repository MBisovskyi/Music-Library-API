from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SongSerializer
from .models import Song
from rest_framework import status

# Create your views here.
@api_view(['GET'], ['POST'])
def songs_list(request):
    if request.method == 'GET':
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many = True)
        return Response(serializer.data)
