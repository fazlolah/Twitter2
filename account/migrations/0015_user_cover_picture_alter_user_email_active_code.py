# Generated by Django 5.1.3 on 2025-02-27 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_alter_user_email_active_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cover_picture',
            field=models.ImageField(blank=True, null=True, upload_to='cover_pictures/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email_active_code',
            field=models.CharField(default='6O0ZvtBDD66bYHnQXnqALHzne8f6SlKUclaNFxofTboSdJ80pBo6bhmPnAce6lHq', max_length=64),
        ),
    ]
