import logging
import os
import tempfile
import zipfile
from wsgiref.util import FileWrapper

from django.db.models import Q
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from accounts.models import Album

logger = logging.getLogger(__name__)


class DownloadAlbumView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        album_id = kwargs.get('album_id')
        user = request.user

        album_query = Album.objects.filter(
            Q(id=album_id),
            Q(creator=user) | Q(users=user)
        )

        if not album_query.exists():
            return HttpResponse('Album not found or access denied.', status=404)

        album = album_query.first()

        files = album.files.all()
        if not files:
            return HttpResponse('No files to download.', status=404)

        missing_files = []
        try:
            with tempfile.NamedTemporaryFile(mode='w+b', delete=False, suffix='.zip') as tmp:
                temp_zip_path = tmp.name
                with zipfile.ZipFile(temp_zip_path, 'w') as zipf:
                    for user_file in files:
                        if not user_file.file:
                            missing_files.append(user_file.id)
                            logger.error(f'Missing file for UserFile id: {user_file.id}')
                            continue
                        file_path = user_file.file.path
                        try:
                            zipf.write(file_path, arcname=os.path.basename(file_path))
                        except FileNotFoundError:
                            missing_files.append(user_file.id)
                            logger.error(
                                f'File not found on disk for UserFile id: {user_file.id}, expected path: {file_path}')
                            continue

                if len(missing_files) == len(files):
                    return HttpResponse('All files in the album are missing.', status=404)

                wrapper = FileWrapper(open(temp_zip_path, 'rb'))
                response = HttpResponse(wrapper, content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename="album_{album_id}.zip"'
                response['Content-Length'] = os.path.getsize(temp_zip_path)
                return response
        except Exception as e:
            logger.error(f'Error creating zip file: {e}')
            return HttpResponse('Error creating zip file.', status=500)
        finally:
            os.remove(temp_zip_path)
