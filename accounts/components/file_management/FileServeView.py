from django.http import HttpResponse, Http404, HttpResponseForbidden
import io
import logging
import mimetypes
import os
from urllib.parse import quote
from moviepy.editor import VideoFileClip

import rawpy
from PIL import Image
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseForbidden

from accounts.models import UserFile

logger = logging.getLogger(__name__)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class FileServeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_path):
        logger.debug(f"Requested file path: {file_path}")
        preview_requested = 'preview' in file_path.split('/')
        original_file_path = file_path.replace('/preview', '')
        logger.debug('test3')
        print('test')
        safe_file_path = os.path.normpath(os.path.join(settings.BASE_DIR, 'uploads', original_file_path))
        cached_directory = os.path.join(os.path.dirname(safe_file_path), 'cached')
        os.makedirs(cached_directory, exist_ok=True)
        filename_without_extension, extension = os.path.splitext(os.path.basename(safe_file_path))
        cached_file_name = f"{filename_without_extension}_preview.png" if preview_requested else os.path.basename(
            safe_file_path)
        cached_file_path = os.path.join(cached_directory, cached_file_name)

        logger.debug(
            f"Preview requested: {preview_requested}, Safe path: {safe_file_path}, Cached path: {cached_file_path}")

        if not os.path.exists(safe_file_path):
            raise Http404("File does not exist.")

        path_parts = original_file_path.split('/')
        if len(path_parts) < 2 or not path_parts[0].startswith('user_'):
            raise Http404("Invalid file path format.")

        user_id_from_path = int(path_parts[0].split('_')[1])
        if user_id_from_path != request.user.id:
            try:
                user_file = UserFile.objects.get(file=original_file_path)
                album = user_file.album
                if album and (request.user != album.creator and request.user not in album.users.all()):
                    raise HttpResponseForbidden("You do not have access to this file.")
            except UserFile.DoesNotExist:
                raise HttpResponseForbidden("You do not have access to this file.")
        logger.debug('test1')
        path_parts = original_file_path.split('/')
        if len(path_parts) < 2 or not path_parts[0].startswith('user_'):
            raise Http404("Invalid file path format.")
        user_id = path_parts[0].split('_')[1]
        try:
            user_id = int(user_id)
            user = User.objects.get(id=user_id)
        except (ValueError, User.DoesNotExist):
            raise Http404("User does not exist.")

        if os.path.exists(cached_file_path):
            with open(cached_file_path, 'rb') as file:
                return HttpResponse(file.read(), content_type="image/png")

        logger.debug('test')
        if preview_requested:
            extension = os.path.splitext(safe_file_path)[1].lower()
            if extension in ['.mp4', '.mov']:
                try:
                    clip = VideoFileClip(safe_file_path)
                    frame = clip.get_frame(1)  # Получаем кадр на 1 секунде видео
                    image = Image.fromarray(frame)
                    image.thumbnail((200, 200))  # Меняем размер до миниатюры
                    buffer = io.BytesIO()
                    image.save(buffer, format="PNG")
                    buffer.seek(0)
                    with open(cached_file_path, 'wb') as f:
                        f.write(buffer.getvalue())
                    return HttpResponse(buffer.getvalue(), content_type="image/png")
                except Exception as e:
                    logger.error(f"Error processing video file: {e}")
                    raise Http404(f"Error processing video file: {e}")

        if preview_requested and extension.lower() in ['.dng', '.raw']:
            try:
                with rawpy.imread(safe_file_path) as raw:
                    rgb_image = raw.postprocess()
                image = Image.fromarray(rgb_image)
                image.thumbnail((200, 200))
                buffer = io.BytesIO()
                image.save(buffer, format="PNG")
                buffer.seek(0)
                with open(cached_file_path, 'wb') as f:
                    f.write(buffer.getvalue())
                return HttpResponse(buffer.getvalue(), content_type="image/png")
            except Exception as e:
                logger.error(f"Error processing RAW file: {e}")
                raise Http404(f"Error processing file: {e}")



        if preview_requested:
            try:
                with Image.open(safe_file_path) as img:
                    img.thumbnail((200, 200))
                    buffer = io.BytesIO()
                    img.save(buffer, format="PNG")
                    buffer.seek(0)
                    with open(cached_file_path, 'wb') as f:
                        f.write(buffer.getvalue())
                    return HttpResponse(buffer.getvalue(), content_type="image/png")
            except Exception as e:
                raise Http404(f"Error processing file: {e}")

        if original_file_path.endswith('/'):
            original_file_path = original_file_path[:-1]

        if original_file_path.endswith(('.dng', '.raw')):
            try:
                with rawpy.imread(safe_file_path) as raw:
                    rgb_image = raw.postprocess()
                image = Image.fromarray(rgb_image)
                if preview_requested:
                    image.thumbnail((200, 200))
                buffer = io.BytesIO()
                image.save(buffer, format="PNG")
                buffer.seek(0)
                with open(cached_file_path, 'wb') as f:
                    f.write(buffer.getvalue())
                return HttpResponse(buffer.getvalue(), content_type="image/png")
            except Exception as e:
                raise Http404(f"Error processing file: {e}")

        mime_type, _ = mimetypes.guess_type(safe_file_path)
        try:
            with open(safe_file_path, 'rb') as file:
                content = file.read()
                response = HttpResponse(content, content_type=mime_type or 'application/octet-stream')
                response['Content-Disposition'] = 'inline; filename="%s"' % quote(os.path.basename(cached_file_path))
                return response
        except IOError:
            raise Http404("Error in reading file.")
