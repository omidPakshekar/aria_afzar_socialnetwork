# Generated by Django 3.2 on 2022-09-06 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_rename_message_supportmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportmessage',
            name='message_type',
            field=models.CharField(blank=True, choices=[('Support', 'Support'), ('Deposit', 'Deposit'), ('Error Reporting', 'Error Reporting')], max_length=20),
        ),
    ]
