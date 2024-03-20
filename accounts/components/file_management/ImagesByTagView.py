from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from accounts.models import UserFile, Tag


class ImagesByTagView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tag_name = request.GET.get('tag')
        if not tag_name:
            return JsonResponse({'error': 'Tag parameter is missing'}, status=400)

        try:
            tag = Tag.objects.get(name=tag_name)
        except Tag.DoesNotExist:
            return JsonResponse({'error': 'Tag not found'}, status=404)

        user_files = UserFile.objects.filter(tags=tag, user=request.user).all()

        images_info = [
            {
                'id': user_file.id,
                'image_url': request.build_absolute_uri(user_file.file.url)
            } for user_file in user_files
        ]

        return JsonResponse({'images': images_info}, safe=False, status=200)
