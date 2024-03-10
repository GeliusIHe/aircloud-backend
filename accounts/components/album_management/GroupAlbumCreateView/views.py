from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.models import Album
import json

@method_decorator(login_required, name='dispatch')
class GroupAlbumCreateView(View):
    def post(self, request):
        data = json.loads(request.body)
        album_name = data.get('name')
        member_usernames = data.get('members', [])

        if not album_name:
            return JsonResponse({'error': 'album_components name is required.'}, status=400)

        album = Album.objects.create(name=album_name, creator=request.user)

        album.users.add(request.user)

        for username in member_usernames:
            try:
                user = User.objects.get(username=username)
                album.users.add(user)
            except User.DoesNotExist:
                return JsonResponse({'error': f'User {username} does not exist.'}, status=404)

        return JsonResponse({'message': 'Group album created successfully.', 'album_id': album.id}, status=201)
