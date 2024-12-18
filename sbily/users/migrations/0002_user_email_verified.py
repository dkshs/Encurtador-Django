# Generated by Django 5.0.10 on 2024-12-18 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False, help_text='Designates whether the user has verified their email address.', verbose_name='email verified'),
        ),
    ]
