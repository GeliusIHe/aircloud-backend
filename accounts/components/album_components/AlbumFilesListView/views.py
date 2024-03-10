from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserFile, Album
from accounts.serializers import UserFileSerializer
from django.db.models import Q


class AlbumFilesListView(ListAPIView):
    serializer_class = UserFileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        album_id = self.kwargs['album_id']
        user = self.request.user

        album_exists = Album.objects.filter(
            Q(id=album_id),
            Q(creator=user) | Q(users=user)
        ).exists()

        if album_exists:
            return UserFile.objects.filter(album__id=album_id)
        else:
            return UserFile.objects.none()
