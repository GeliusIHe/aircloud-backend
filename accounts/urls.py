from django.urls import path

from accounts.components.album_components.AlbumCreateView import AlbumCreateView
from accounts.components.album_components.AlbumFileDeleteView import AlbumFileDeleteView
from accounts.components.album_components.AlbumFileUploadView import AlbumFileUploadView
from accounts.components.album_components.AlbumFilesListView import AlbumFilesListView
from accounts.components.file_management.FileTagEditView import FileTagEditView
from accounts.components.album_management.GroupAlbumCreateView import GroupAlbumCreateView
from accounts.components.album_management.GroupAlbumMembersView import GroupAlbumMembersView
from accounts.components.authentication.RegisterView import RegisterView
from accounts.components.authentication.LoginView import LoginView
from accounts.components.file_management.FileUploadView import UserFileListView
from .components.album_components.UserAlbumsView import UserAlbumsView
from .components.file_management.DownloadAlbumView import DownloadAlbumView
from .components.file_management.DownloadSelectedPhotosView import DownloadSelectedPhotosView
from .components.file_management.ImagesByTagView import ImagesByTagView
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
    path('download_selected_photos/', DownloadSelectedPhotosView.as_view(), name='download_selected_photos'),
    path('user_albums/', UserAlbumsView.as_view(), name='user_albums'),
]
