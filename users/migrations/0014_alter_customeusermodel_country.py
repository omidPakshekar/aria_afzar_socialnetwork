# Generated by Django 3.2 on 2022-09-03 15:58

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20220903_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeusermodel',
            name='country',
            field=django_countries.fields.CountryField(default=1, max_length=2),
            preserve_default=False,
        ),
    ]