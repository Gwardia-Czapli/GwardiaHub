# Generated by Django 5.0.3 on 2024-05-11 13:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gwardia", "0004_rename_nextmeeting_meeting"),
    ]

    operations = [
        migrations.AddField(
            model_name="meeting",
            name="duration",
            field=models.CharField(default="0oO"),
        ),
    ]
