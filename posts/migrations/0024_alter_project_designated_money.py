# Generated by Django 3.2 on 2022-09-12 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0023_alter_project_preferred_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='designated_money',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=12, null=True),
        ),
    ]
