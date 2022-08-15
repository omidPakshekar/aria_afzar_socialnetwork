# Generated by Django 3.2.15 on 2022-08-13 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_delete_membership'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_system',
            field=models.CharField(choices=[('Bitcoin', 'Bitcoin'), ('Visa', 'Visa'), ('Ether', 'Ether')], default='Pending', max_length=20),
        ),
    ]