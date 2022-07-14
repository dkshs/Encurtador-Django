# Generated by Django 4.0.6 on 2022-07-14 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Link",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("link_redirecionado", models.URLField()),
                ("link_encurtado", models.CharField(max_length=8, unique=True)),
            ],
        ),
    ]
