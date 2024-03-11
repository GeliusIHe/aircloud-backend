from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import UserFile, Album

@method_decorator(login_required, name='dispatch')
class AlbumFileUploadView(View):
    def post(self, request):
        file = request.FILES.get('file')
        file_type = request.POST.get('file_type', 'photo')
        album_id = request.POST.get('album_id')

        album_query = Album.objects.filter(id=album_id).filter(Q(creator=request.user) | Q(users=request.user))

        if not album_query.exists():
            return JsonResponse({'error': 'You do not have access to this album or it does not exist.'}, status=403)

        album = album_query.first()

        if file is not None:
            user_file = UserFile(user=request.user, file=file, file_type=file_type, album=album)
            user_file.save()
        else:
            return JsonResponse({'error': 'The file was not provided.'}, status=400)

        return JsonResponse({'message': f'The file has been successfully uploaded to the album.'}, status=201)
