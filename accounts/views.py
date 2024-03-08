from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import UserFile
from rest_framework.generics import ListAPIView
from accounts.models import Album
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @staticmethod
    def post(request):
        file = request.data.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user_file = UserFile(user=user, file=file)
        user_file.save()

        return Response({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)


class AlbumMembersListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        album_id = self.kwargs.get('album_id')
        album = Album.objects.get(id=album_id)
        return album.users.all()
