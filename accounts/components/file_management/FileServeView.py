from django.http import HttpResponse, Http404
from django.views import View
from django.conf import settings
from django.contrib.auth.models import User
from accounts.models import Album
import rawpy
import os
import mimetypes
from PIL import Image
import io
from urllib.parse import quote

class FileServeView(View):
    def get(self, request, file_path):
        preview_requested = 'preview' in file_path.split('/')
        original_file_path = file_path.replace('/preview', '')

        safe_file_path = os.path.normpath(os.path.join(settings.BASE_DIR, 'uploads', original_file_path))
        cached_directory = os.path.join(os.path.dirname(safe_file_path), 'cached')
        os.makedirs(cached_directory, exist_ok=True)
        filename_without_extension, extension = os.path.splitext(os.path.basename(safe_file_path))
        cached_file_path = os.path.join(cached_directory, filename_without_extension + ('_preview.png' if preview_requested else extension))

        path_parts = original_file_path.split('/')
        if len(path_parts) < 2 or not path_parts[0].startswith('user_'):
            raise Http404("Invalid file path format.")
        user_id = path_parts[0].split('_')[1]
        try:
            user_id = int(user_id)
            user = User.objects.get(id=user_id)
        except (ValueError, User.DoesNotExist):
            raise Http404("User does not exist.")

        if request.user != user and not Album.objects.filter(users=request.user, files__file__endswith=original_file_path).exists():
            raise Http404("You do not have permission to access this file.")

        if os.path.exists(cached_file_path):
            with open(cached_file_path, 'rb') as file:
                return HttpResponse(file.read(), content_type="image/png")

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
