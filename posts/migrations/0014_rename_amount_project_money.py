# Generated by Django 3.2 on 2022-09-10 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_demand_suggested_money'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='amount',
            new_name='money',
        ),
    ]
