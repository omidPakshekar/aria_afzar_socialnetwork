# Generated by Django 3.2 on 2022-09-10 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_rename_money_holdprojectmoney_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='suggested_money',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=12),
        ),
    ]
