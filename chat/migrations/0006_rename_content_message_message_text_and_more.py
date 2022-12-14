# Generated by Django 4.1 on 2022-08-24 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_alter_contact_friends_alter_contact_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='content',
            new_name='message_text',
        ),
        migrations.RemoveField(
            model_name='message',
            name='contact',
        ),
        migrations.AddField(
            model_name='message',
            name='parent_message',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child', to='chat.message'),
        ),
        migrations.RemoveField(
            model_name='chat',
            name='participants',
        ),
        migrations.AddField(
            model_name='chat',
            name='participants',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='chats', to='chat.contact'),
            preserve_default=False,
        ),
    ]
