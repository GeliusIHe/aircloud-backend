# Generated by Django 5.0.3 on 2024-03-08 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_files_userfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfile',
            name='file_type',
            field=models.CharField(choices=[('photo', 'Photo'), ('video', 'Video')], default='photo', max_length=5),
            preserve_default=False,
        ),
    ]
