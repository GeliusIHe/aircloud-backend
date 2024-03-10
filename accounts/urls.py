from django.urls import path

from accounts.components.album_components.AlbumCreateView.views import AlbumCreateView
from accounts.components.album_components.AlbumFileDeleteView.views import AlbumFileDeleteView
from accounts.components.album_components.AlbumFileUploadView.views import AlbumFileUploadView
from accounts.components.album_components.AlbumFilesListView.views import AlbumFilesListView
from accounts.components.file_management.FileTagEditView.views import FileTagEditView
from accounts.components.album_management.GroupAlbumCreateView.views import GroupAlbumCreateView
from accounts.components.album_management.GroupAlbumMembersView.views import GroupAlbumMembersView
from accounts.components.authentication.RegisterView.views import RegisterView
from accounts.components.authentication.LoginView.views import LoginView
from accounts.components.file_management.FileUploadView.views import UserFileListView
from .components.file_management.DownloadAlbumView.views import DownloadAlbumView
from .components.file_management.ImagesByTagView.views import ImagesByTagView
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
    path('album/<int:album_id>/delete-file/<int:file_id>/', AlbumFileDeleteView.as_view(),
         name='delete_file_from_album'),
    path('file/tags/', FileTagEditView.as_view(), name='file_tags_edit'),
    path('file/tags/<int:file_id>/', FileTagEditView.as_view(), name='file_tags_edit'),
    path('images-by-tag/', ImagesByTagView.as_view(), name='images_by_tag'),
    path('albums/<int:album_id>/download/', DownloadAlbumView.as_view(), name='download-album'),
]
