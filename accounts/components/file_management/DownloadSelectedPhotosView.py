import json
import logging
import os
import tempfile
import zipfile
from wsgiref.util import FileWrapper

from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from accounts.models import UserFile

logger = logging.getLogger(__name__)

class DownloadSelectedPhotosView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            photo_ids = json.loads(request.body).get('photo_ids', [])
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if not photo_ids:
            return JsonResponse({'error': 'No photo IDs provided'}, status=400)

        photos = UserFile.objects.filter(id__in=photo_ids, user=request.user)

        if not photos.exists():
            return HttpResponse('No photos found or access denied.', status=404)

        try:
            with tempfile.NamedTemporaryFile(mode='w+b', delete=False, suffix='.zip') as tmp:
                temp_zip_path = tmp.name
                with zipfile.ZipFile(temp_zip_path, 'w') as zipf:
                    for photo in photos:
                        try:
                            file_path = photo.file.path
                            zipf.write(file_path, arcname=os.path.basename(file_path))
                        except FileNotFoundError:
                            return HttpResponse(f'File not found: {photo.file.name}', status=404)
                        except ValueError:
                            logger.error(f'File attribute has no file associated with it: {photo.file.name}')
                            continue
                        except Exception as e:
                            return HttpResponse(f'Error processing file {photo.file.name}: {e}', status=500)

                wrapper = FileWrapper(open(temp_zip_path, 'rb'))
                response = HttpResponse(wrapper, content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename="selected_photos.zip"'
                response['Content-Length'] = os.path.getsize(temp_zip_path)
                return response
        finally:
            os.remove(temp_zip_path)

