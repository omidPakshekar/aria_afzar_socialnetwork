# Generated by Django 3.2 on 2022-09-04 08:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_customeusermodel_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivationKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.PositiveSmallIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_activation_key', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
