import json
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import zipfile
import tempfile
from wsgiref.util import FileWrapper
import os
from accounts.models import UserFile
import logging

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class DownloadSelectedPhotosView(View):
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

