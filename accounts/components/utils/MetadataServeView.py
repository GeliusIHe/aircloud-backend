import json
import os

from django.conf import settings
from django.http import JsonResponse, Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from accounts.models import User, Album


class MetadataServeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, filename):
        metadata_file_path = os.path.join(settings.BASE_DIR, 'uploads', f'user_{user_id}', f'{filename}.json')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("User does not exist.")

        if request.user != user and not Album.objects.filter(users=request.user, files__file__contains=f'user_{user_id}/{filename}').exists():
            raise Http404("You do not have permission to access this file.")

        try:
            with open(metadata_file_path, 'r') as file:
                metadata = json.load(file)
                return JsonResponse(metadata)
        except IOError:
            raise Http404("Metadata file not found or error in reading file.")
