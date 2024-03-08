from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.models import UserFile, Album

@method_decorator(login_required, name='dispatch')
class AlbumFileUploadView(View):
    def post(self, request):
        file = request.FILES.get('file')
        file_type = request.POST.get('file_type', 'photo')
        album_id = request.POST.get('album_id')

        try:
            album = Album.objects.get(id=album_id, user=request.user)
        except Album.DoesNotExist:
            return JsonResponse({'error': 'Album does not exist.'}, status=404)

        user_file = UserFile(user=request.user, file=file, file_type=file_type, album=album)
        user_file.save()

        return JsonResponse({'message': 'File uploaded to album successfully.'}, status=201)
