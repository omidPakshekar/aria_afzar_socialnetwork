# Generated by Django 3.2.15 on 2022-08-16 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0002_podcast_is_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuccessfulExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('like', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='successful_experience', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
