# Generated by Django 5.1.1 on 2025-02-21 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("animals", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="animal",
            name="name",
        ),
    ]
