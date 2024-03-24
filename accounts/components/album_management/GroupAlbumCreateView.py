from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User
from accounts.models import Album
import json

class GroupAlbumCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        album_name = data.get('name')
        member_usernames = data.get('members', [])

        if not album_name:
            return JsonResponse({'error': 'Album name is required.'}, status=400)

        album = Album.objects.create(name=album_name, creator=request.user)
        album.users.add(request.user)
        album = Album.objects.create(name=album_name, creator=request.user,
                                     is_private=False)  # для групповых альбомов устанавливаем is_private в False

        for username in member_usernames:
            try:
                user = User.objects.get(username=username)
                album.users.add(user)
            except User.DoesNotExist:
                return JsonResponse({'error': f'User {username} does not exist.'}, status=404)

        return JsonResponse({'message': 'Group album created successfully.', 'album_id': album.id}, status=201)
