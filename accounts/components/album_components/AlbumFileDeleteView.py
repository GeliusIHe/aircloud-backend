from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from accounts.models import UserFile, Album


class AlbumFileDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        file_id = kwargs.get('file_id')
        album_id = kwargs.get('album_id')

        try:
            album = Album.objects.get(id=album_id, creator=request.user)
            user_file = UserFile.objects.get(id=file_id, album=album, user=request.user)
            user_file.delete()
            return JsonResponse({'message': 'File deleted from album successfully.'}, status=200)
        except Album.DoesNotExist:
            return JsonResponse({'error': 'Album does not exist or you do not have permission to access it.'}, status=404)
        except UserFile.DoesNotExist:
            return JsonResponse({'error': 'File does not exist or you do not have permission to access it.'}, status=404)
