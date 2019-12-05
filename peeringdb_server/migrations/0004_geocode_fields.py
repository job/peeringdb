# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-24 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("peeringdb_server", "0003_add_lat_lon_to_address_models"),
    ]

    operations = [
        migrations.AddField(
            model_name="facility",
            name="geocode_date",
            field=models.DateTimeField(
                blank=True, help_text=b"Last time of attempted geocode", null=True
            ),
        ),
        migrations.AddField(
            model_name="facility",
            name="geocode_error",
            field=models.TextField(
                blank=True,
                help_text=b"Error message of previous geocode attempt",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="facility",
            name="geocode_status",
            field=models.BooleanField(
                default=False,
                help_text=b"Has this object's latitude and longitude been syncronized to it's address fields",
            ),
        ),
    ]
