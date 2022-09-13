# Generated by Django 3.2 on 2022-09-10 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_rename_amount_project_money'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='money',
        ),
        migrations.AddField(
            model_name='project',
            name='designated_money',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='project',
            name='money_max',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='project',
            name='money_min',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=12),
        ),
    ]