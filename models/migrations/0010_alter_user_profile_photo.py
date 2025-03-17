# Generated by Django 5.1.6 on 2025-03-17 08:12

import utils.file_uploader
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0009_alter_user_bio_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(blank=True, default='static/images/users/default.png', upload_to=utils.file_uploader.uploaded_file_path, verbose_name='Фото профиля'),
        ),
    ]
