# Generated by Django 3.2.15 on 2022-08-19 10:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0002_auto_20220819_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='podcast',
            name='user_liked',
            field=models.ManyToManyField(related_name='podcasts_liked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='user_liked',
            field=models.ManyToManyField(related_name='posts_liked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='user_saved',
            field=models.ManyToManyField(related_name='posts_saved', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='successfullexperience',
            name='user_liked',
            field=models.ManyToManyField(related_name='exprience_liked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='successfullexperience',
            name='user_saved',
            field=models.ManyToManyField(related_name='exprience_saved', to=settings.AUTH_USER_MODEL),
        ),
    ]
