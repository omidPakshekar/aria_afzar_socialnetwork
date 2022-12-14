# Generated by Django 3.2 on 2022-08-29 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20220829_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeusermodel',
            name='profile_pic',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profileimage'),
        ),
        migrations.AddField(
            model_name='customeusermodel',
            name='user_bio',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.userbio'),
        ),
    ]
