from django.http import HttpResponse, Http404
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import zipfile
import os
from wsgiref.util import FileWrapper
from django.db.models import Q

from accounts.models import Album, UserFile

import logging
logger = logging.getLogger(__name__)

@method_decorator(login_required, name='dispatch')
class DownloadAlbumView(View):
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

        temp_zip_path = '/tmp/album_{}.zip'.format(album_id)

        try:
            with zipfile.ZipFile(temp_zip_path, 'w') as zipf:
                for user_file in files:
                    file_path = user_file.file.path
                    try:
                        zipf.write(file_path, arcname=os.path.basename(file_path))
                    except FileNotFoundError:
                        logger.error(f'File not found: {user_file.file.path}')
                        continue
        except Exception as e:
            logger.error(f'Error creating zip file: {e}')
            return HttpResponse('Error creating zip file.', status=500)

        try:
            wrapper = FileWrapper(open(temp_zip_path, 'rb'))
            response = HttpResponse(wrapper, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(temp_zip_path))
            response['Content-Length'] = os.path.getsize(temp_zip_path)
            return response
        finally:
            os.remove(temp_zip_path)
