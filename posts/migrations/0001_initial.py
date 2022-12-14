# Generated by Django 3.2.15 on 2022-08-22 07:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import posts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SuccessfullExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('admin_check', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='successfullexperience_related', to=settings.AUTH_USER_MODEL)),
                ('user_liked', models.ManyToManyField(blank=True, related_name='exprience_liked', to=settings.AUTH_USER_MODEL)),
                ('user_saved', models.ManyToManyField(blank=True, related_name='exprience_saved', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('admin_check', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, default=posts.models.get_default_post_image, max_length=255, null=True, upload_to=posts.models.get_post_image_filepath)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_related', to=settings.AUTH_USER_MODEL)),
                ('user_liked', models.ManyToManyField(blank=True, related_name='post_liked', to=settings.AUTH_USER_MODEL)),
                ('user_saved', models.ManyToManyField(blank=True, related_name='post_saved', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('admin_check', models.BooleanField(default=False)),
                ('file', models.FileField(upload_to=posts.models.get_podcast_filepath)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='podcast_related', to=settings.AUTH_USER_MODEL)),
                ('user_liked', models.ManyToManyField(blank=True, related_name='podcast_liked', to=settings.AUTH_USER_MODEL)),
                ('user_saved', models.ManyToManyField(blank=True, related_name='podcast_saved', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('comment_text', models.TextField(blank=True, max_length=100, null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('admin_check', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(limit_choices_to={'model__in': ('post', 'podcast', 'successfullexperience')}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('user_liked', models.ManyToManyField(blank=True, related_name='comment_liked', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_time'],
            },
        ),
    ]
