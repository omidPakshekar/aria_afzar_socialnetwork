# Generated by Django 3.2 on 2022-09-12 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0021_rename_preferred_time_project_preferred_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='money_max',
            field=models.DecimalField(decimal_places=4, max_digits=12),
        ),
        migrations.AlterField(
            model_name='project',
            name='money_min',
            field=models.DecimalField(decimal_places=4, max_digits=12),
        ),
    ]
