# Generated by Django 3.2 on 2022-09-12 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0024_alter_project_designated_money'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='designated_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]