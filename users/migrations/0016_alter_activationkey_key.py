# Generated by Django 3.2 on 2022-09-04 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_activationkey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activationkey',
            name='key',
            field=models.IntegerField(),
        ),
    ]
