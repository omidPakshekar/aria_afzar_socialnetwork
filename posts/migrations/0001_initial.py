# Generated by Django 3.2.15 on 2022-08-19 12:09

from django.db import migrations, models
import django.db.models.deletion
import posts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('admin_check', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('itembase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='posts.itembase')),
                ('file', models.FileField(blank=True, default=posts.models.get_default_post_image, null=True, upload_to=posts.models.get_post_image_filepath)),
            ],
            bases=('posts.itembase',),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('itembase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='posts.itembase')),
                ('image', models.ImageField(blank=True, default=posts.models.get_default_post_image, max_length=255, null=True, upload_to=posts.models.get_post_image_filepath)),
            ],
            bases=('posts.itembase',),
        ),
        migrations.CreateModel(
            name='SuccessfullExperience',
            fields=[
                ('itembase_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='posts.itembase')),
            ],
            bases=('posts.itembase',),
        ),
    ]
