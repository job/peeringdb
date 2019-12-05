# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-21 05:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("peeringdb_server", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Partnership",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "level",
                    models.PositiveIntegerField(
                        choices=[(1, "Data Validation Partner"), (2, "RIR Partner")],
                        default=1,
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        blank=True,
                        help_text="If specified clicking the partnership will take the user to this location",
                        null=True,
                        verbose_name="URL",
                    ),
                ),
                (
                    "logo",
                    models.FileField(
                        blank=True,
                        help_text=b"Allows you to upload and set a logo image file for this partnership",
                        null=True,
                        upload_to=b"logos/",
                    ),
                ),
                (
                    "org",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="partnerships",
                        to="peeringdb_server.Organization",
                    ),
                ),
            ],
            options={
                "db_table": "peeringdb_partnership",
                "verbose_name": "Partnership",
                "verbose_name_plural": "Partnerships",
            },
        ),
    ]
