# Generated by Django 5.0.10 on 2024-12-22 02:25

import django.core.validators
import django.db.models.deletion
import sbily.links.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0003_shortenedlink_remove_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shortenedlink',
            options={'ordering': ['-created_at'], 'verbose_name': 'Shortened Link', 'verbose_name_plural': 'Shortened Links'},
        ),
        migrations.AlterField(
            model_name='shortenedlink',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, help_text='When this shortened link was created', verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='shortenedlink',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, help_text='Whether this shortened link is active', verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='shortenedlink',
            name='original_link',
            field=models.URLField(help_text='The original URL that will be shortened', max_length=2000, verbose_name='Original URL'),
        ),
        migrations.AlterField(
            model_name='shortenedlink',
            name='remove_at',
            field=models.DateTimeField(blank=True, db_index=True, help_text='When this link should be automatically removed', null=True, validators=[sbily.links.models.future_date_validator], verbose_name='Remove At'),
        ),
        migrations.AlterField(
            model_name='shortenedlink',
            name='shortened_link',
            field=models.CharField(blank=True, db_index=True, help_text='The shortened URL path', max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Shortened link must be alphanumeric with hyphens and underscores only', regex='^[a-zA-Z0-9-_]*$')], verbose_name='Shortened URL'),
        ),
        migrations.AlterField(
            model_name='shortenedlink',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='When this shortened link was last updated', verbose_name='Updated At'),
        ),
        migrations.AlterField(
            model_name='shortenedlink',
            name='user',
            field=models.ForeignKey(help_text='User who created this shortened link', on_delete=django.db.models.deletion.CASCADE, related_name='shortened_links', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='shortenedlink',
            index=models.Index(fields=['shortened_link', 'user'], name='links_short_shorten_71809b_idx'),
        ),
    ]