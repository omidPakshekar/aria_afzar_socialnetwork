# Generated by Django 4.1 on 2022-08-24 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_remove_message_author_message_owner_contact_chat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='user',
            new_name='owner',
        ),
    ]
