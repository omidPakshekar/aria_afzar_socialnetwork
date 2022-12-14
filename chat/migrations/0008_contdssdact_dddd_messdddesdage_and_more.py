# Generated by Django 4.1 on 2022-08-24 13:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0007_message_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contdssdact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friends', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='dddd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Messdddesdage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_messages', to=settings.AUTH_USER_MODEL)),
                ('parent_message', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child', to='chat.messdddesdage')),
            ],
        ),
        migrations.RemoveField(
            model_name='contact',
            name='friends',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='message',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='message',
            name='parent_message',
        ),
        migrations.DeleteModel(
            name='Chat',
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.AddField(
            model_name='dddd',
            name='messages',
            field=models.ManyToManyField(blank=True, to='chat.messdddesdage'),
        ),
        migrations.AddField(
            model_name='dddd',
            name='participants',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='chats', to='chat.contdssdact'),
        ),
    ]
