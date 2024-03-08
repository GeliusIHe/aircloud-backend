from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    # Путь для хранения файла будет uploads/user_<user_id>/<filename>
    return 'uploads/user_{0}/{1}'.format(instance.user.id, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    files = models.FileField(upload_to=user_directory_path, null=True, blank=True)

class Album(models.Model):
    users = models.ManyToManyField(User, related_name='albums')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=True)
    creator = models.ForeignKey(User, related_name='created_albums', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
class AlbumMember(models.Model):
    album = models.ForeignKey(Album, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='album_memberships', on_delete=models.CASCADE)
    is_creator = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} -> {self.album.name}"
class UserFile(models.Model):
    FILE_TYPES = (
        ('photo', 'Photo'),
        ('video', 'Video'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    file_type = models.CharField(max_length=5, choices=FILE_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='files', null=True, blank=True)  # Добавленная строка


