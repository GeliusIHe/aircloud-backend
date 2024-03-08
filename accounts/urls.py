from django.urls import path

from .components.AlbumCreateView.views import AlbumCreateView
from .components.AlbumFileUploadView.views import AlbumFileUploadView
from .components.AlbumFilesListView.views import AlbumFilesListView
from .components.GroupAlbumCreateView.views import GroupAlbumCreateView
from .components.GroupAlbumMembersView.views import GroupAlbumMembersView
from .components.RegisterView.views import RegisterView
from .components.LoginView.views import LoginView
from .components.FileUploadView.views import UserFileListView
from .views import FileUploadView, AlbumMembersListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='RegisterView'),
    path('login/', LoginView.as_view(), name='LoginView'),
    path('upload/', FileUploadView.as_view(), name='file-FileUploadView'),
    path('files/', UserFileListView.as_view(), name='user-files'),
    path('albums/create/', AlbumCreateView.as_view(), name='album-create'),
    path('upload-to-album/', AlbumFileUploadView.as_view(), name='FileUploadView-to-album'),
    path('albums/<int:album_id>/files/', AlbumFilesListView.as_view(), name='album-files-list'),
    path('group-albums/create/', GroupAlbumCreateView.as_view(), name='group-album-create'),
    path('group-albums/<int:album_id>/members/', GroupAlbumMembersView.as_view(), name='group-album-members'),
    path('albums/<int:album_id>/members/', AlbumMembersListView.as_view(), name='album-members-list'),
]
