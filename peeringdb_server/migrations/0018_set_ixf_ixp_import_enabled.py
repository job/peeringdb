# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-03-20 08:09
from __future__ import unicode_literals

from django.db import migrations, models


def forwards_func(apps, schema_editor):
    model = apps.get_model("peeringdb_server", "IXLan")
    for ixlan in model.objects.all():
        if ixlan.ixf_ixp_member_list_url:
            ixlan.ixf_ixp_import_enabled = True
            ixlan.save()


class Migration(migrations.Migration):

    dependencies = [
        ("peeringdb_server", "0017_ixf_ixp_import_enabled"),
    ]

    operations = [
        migrations.AlterModelManagers(name="ixlan", managers=[],),
        migrations.RunPython(forwards_func, migrations.RunPython.noop),
    ]
