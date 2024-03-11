from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from accounts.models import UserFile, Album

@method_decorator(login_required, name='dispatch')
class AlbumFileDeleteView(View):
    def delete(self, request, *args, **kwargs):
        file_id = kwargs.get('file_id')
        album_id = kwargs.get('album_id')

        try:
            album = Album.objects.get(id=album_id, user=request.user)
            user_file = UserFile.objects.get(id=file_id, album=album, user=request.user)
            user_file.delete()
            return JsonResponse({'message': 'File deleted from album successfully.'}, status=200)
        except Album.DoesNotExist:
            return JsonResponse({'error': 'album_components does not exist or you do not have permission to access it.'}, status=404)
        except UserFile.DoesNotExist:
            return JsonResponse({'error': 'File does not exist or you do not have permission to access it.'}, status=404)
