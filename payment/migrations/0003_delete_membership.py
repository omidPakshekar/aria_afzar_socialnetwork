# Generated by Django 3.2.15 on 2022-08-12 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_membership'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MemberShip',
        ),
    ]