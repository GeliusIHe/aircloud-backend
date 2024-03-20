from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from accounts.models import UserFile
from accounts.serializers import UserFileSerializer


class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file')
        file_type = request.POST.get('file_type', 'photo')
        user_file = UserFile(user=request.user, file=file, file_type=file_type)
        user_file.save()
        return JsonResponse({'message': 'File uploaded successfully'}, status=201)
class UserFileListView(ListAPIView):
    serializer_class = UserFileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserFile.objects.filter(user=self.request.user)
