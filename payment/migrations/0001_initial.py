# Generated by Django 3.2.15 on 2022-08-18 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PiggyBank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=4, max_digits=12)),
                ('started_time', models.DateTimeField(auto_now_add=True)),
                ('finish_time', models.DateTimeField(auto_now_add=True, verbose_name='date create')),
                ('expired_day', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='date create')),
                ('created_time', models.TimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=4, max_digits=12)),
                ('payment_system', models.CharField(choices=[('Bitcoin', 'Bitcoin'), ('Visa', 'Visa'), ('Ether', 'Ether')], max_length=20)),
                ('status', models.CharField(choices=[('Accept', 'Accept'), ('Reject', 'Reject'), ('Pending', 'Pending')], default='Pending', max_length=20)),
                ('description', models.TextField(blank=True)),
                ('done', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
