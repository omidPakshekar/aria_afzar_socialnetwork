# Generated by Django 3.2 on 2022-09-11 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_alter_transactionhistory_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionhistory',
            name='kind',
            field=models.CharField(choices=[('withdraw', 'withdraw'), ('deposit', 'deposit'), ('listen', 'listen'), ('like', 'like'), ('membership', 'membership'), ('piggy', 'piggy'), ('donate', 'donate'), ('project', 'project')], max_length=20),
        ),
    ]
