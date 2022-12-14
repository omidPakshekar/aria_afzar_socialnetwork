# Generated by Django 3.2 on 2022-09-14 10:39

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0027_alter_comment_comment_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='cover',
            field=models.ImageField(blank=True, default=posts.models.get_default_post_image, max_length=255, null=True, upload_to=posts.models.get_podcast_cover_image_filepath),
        ),
    ]
