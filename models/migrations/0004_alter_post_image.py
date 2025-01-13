# Generated by Django 5.1.4 on 2025-01-12 21:00

import utils.file_uploader
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0003_alter_post_description_alter_post_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='images/posts/default.jpg', upload_to=utils.file_uploader.uploaded_file_path, verbose_name='Изображение'),
        ),
    ]
