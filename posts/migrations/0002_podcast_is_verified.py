# Generated by Django 3.2.15 on 2022-08-16 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]