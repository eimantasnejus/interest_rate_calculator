# Generated by Django 4.2.7 on 2023-11-18 07:55

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calculator", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="loan",
            name="term",
        ),
        migrations.AddField(
            model_name="loan",
            name="start_date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
