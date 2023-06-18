# Generated by Django 4.2 on 2023-04-26 13:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("feed", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="ticket",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="feed.ticket",
            ),
        ),
    ]
