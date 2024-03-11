from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import Album
from accounts.serializers import AlbumSerializer

class UserAlbumsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        albums = Album.objects.filter(Q(creator=user) | Q(users=user)).distinct()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)
