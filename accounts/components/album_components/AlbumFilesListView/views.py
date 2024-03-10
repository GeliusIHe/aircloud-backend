from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserFile, Album
from accounts.serializers import UserFileSerializer

class AlbumFilesListView(ListAPIView):
    serializer_class = UserFileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        album_id = self.kwargs['album_id']
        if Album.objects.filter(id=album_id, users__id=self.request.user.id).exists():
            return UserFile.objects.filter(album__id=album_id)
        else:
            return UserFile.objects.none()
