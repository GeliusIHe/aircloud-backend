import json
import numbers
import os

from PIL import ExifTags, TiffImagePlugin
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from accounts.models import UserFile, Album, user_directory_path_metadata


@method_decorator(login_required, name='dispatch')
class AlbumFileUploadView(View):
    def post(self, request):
        response_data = {'message': 'The file has been successfully uploaded to the album.'}
        file = request.FILES.get('file')
        file_type = request.POST.get('file_type', 'photo')
        album_id = request.POST.get('album_id')

        album_query = Album.objects.filter(id=album_id).filter(Q(creator=request.user) | Q(users=request.user))
        if not album_query.exists():
            return JsonResponse({'error': 'You do not have access to this album or it does not exist.'}, status=403)

        album = album_query.first()

        if file and file_type == 'photo':
            user_file = UserFile(user=request.user, file=file, file_type=file_type, album=album)
            user_file.save()

            try:
                image = Image.open(user_file.file.path)
                if hasattr(image, '_getexif'):
                    exif_info = image._getexif()
                    if exif_info is not None:
                        exif_data = {ExifTags.TAGS.get(key): value for key, value in exif_info.items() if
                                     key in ExifTags.TAGS}
                        serializable_exif_data = exif_to_serializable(exif_data)

                        filename_for_metadata = os.path.splitext(os.path.basename(user_file.file.name))[0] + '.json'

                        metadata_path = user_directory_path_metadata(user_file, filename_for_metadata)
                        os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
                        with open(metadata_path, 'w') as metadata_file:
                            json.dump(serializable_exif_data, metadata_file)
            except Exception as e:
                error_message = f'Failed to extract metadata: {e}'
                print(error_message)
                response_data['metadata_error'] = error_message
        else:
            return JsonResponse({'error': 'The file was not provided or the file type is not supported.'}, status=400)

        return JsonResponse(response_data, status=201)


def exif_to_serializable(exif_data):
    serializable_data = {}
    for key, value in exif_data.items():
        if isinstance(value, TiffImagePlugin.IFDRational):
            serializable_data[key] = float(value)
        elif isinstance(value, tuple) and all(isinstance(n, numbers.Integral) for n in value):
            serializable_data[key] = [float(n) for n in value]
        elif isinstance(value, bytes):
            serializable_data[key] = value.decode('utf-8', 'ignore')
        else:
            try:
                json.dumps(value)
                serializable_data[key] = value
            except TypeError:
                serializable_data[key] = str(value)
    return serializable_data
