import json

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from accounts.models import Album


class AlbumCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        album_name = data.get('name')

        if not album_name:
            return JsonResponse({'error': 'Album name is required.'}, status=400)

        album = Album.objects.create(name=album_name, creator=request.user)

        return JsonResponse({'message': 'Album created successfully.', 'album_id': album.id}, status=201)
