# Generated by Django 5.1.4 on 2025-01-13 20:59

from django.db import migrations, models

import utils.file_uploader


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0005_alter_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='votes_number',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество голосов'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to=utils.file_uploader.uploaded_file_path, verbose_name='Изображение'),
        ),
    ]
