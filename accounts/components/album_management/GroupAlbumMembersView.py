from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User
from accounts.models import Album
import json

class GroupAlbumMembersView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        username = data.get('username')
        action = data.get('action')
        album_id = kwargs.get('album_id')

        if not username or action not in ['add', 'remove']:
            return JsonResponse({'error': 'Invalid data provided.'}, status=400)

        try:
            album = Album.objects.get(id=album_id)

            if request.user != album.creator:
                return JsonResponse({'error': 'You do not have permission to modify this album.'}, status=403)

            user = User.objects.get(username=username)

            if action == 'add':
                if album.users.filter(username=username).exists():
                    return JsonResponse({'error': 'User already a member.'}, status=400)
                album.users.add(user)
                message = 'User added to album successfully.'

            elif action == 'remove':
                if not album.users.filter(username=username).exists():
                    return JsonResponse({'error': 'User not a member of the album.'}, status=400)
                album.users.remove(user)
                message = 'User removed from album successfully.'

            return JsonResponse({'message': message}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist.'}, status=404)
        except Album.DoesNotExist:
            return JsonResponse({'error': 'Album does not exist.'}, status=404)
