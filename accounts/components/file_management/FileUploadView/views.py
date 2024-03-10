from accounts.serializers import UserFileSerializer
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from accounts.models import UserFile

@method_decorator(login_required, name='dispatch')
class FileUploadView(View):
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
