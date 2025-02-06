# Generated by Django 5.1.5 on 2025-02-06 21:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accompany", "0004_travelgroup_gender"),
    ]

    operations = [
        migrations.AddField(
            model_name="travelgroup",
            name="max_age",
            field=models.IntegerField(default=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="travelgroup",
            name="min_age",
            field=models.IntegerField(default=20),
            preserve_default=False,
        ),
    ]
