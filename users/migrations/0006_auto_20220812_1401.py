# Generated by Django 3.2.15 on 2022-08-12 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_wallet_wallet_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customeusermodel',
            name='is_student',
        ),
        migrations.AddField(
            model_name='customeusermodel',
            name='country',
            field=models.CharField(blank=True, choices=[('IR', 'Iran'), ('US', 'United State'), ('UK', 'United Kindom'), ('CH', 'China'), ('BR', 'Brazil'), ('FR', 'French'), ('PL', 'Poland')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='customeusermodel',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True),
        ),
    ]
