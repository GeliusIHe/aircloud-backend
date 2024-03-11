from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.models import Album
import json

@method_decorator(login_required, name='dispatch')
class AlbumCreateView(View):
    def post(self, request):
        data = json.loads(request.body)
        album_name = data.get('name')

        if not album_name:
            return JsonResponse({'error': 'album_components name is required.'}, status=400)

        album = Album.objects.create(name=album_name, creator=request.user)

        return JsonResponse({'message': 'album_components created successfully.', 'album_id': album.id}, status=201)