# Generated by Django 5.0.10 on 2024-12-18 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_token_expires_at'),
    ]

    operations = [
        migrations.RenameIndex(
            model_name='token',
            new_name='users_token_user_id_ea9964_idx',
            old_fields=('user', 'type', 'created_at'),
        ),
    ]