# Generated by Django 3.2.15 on 2022-08-12 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_alter_payment_time'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
    ]