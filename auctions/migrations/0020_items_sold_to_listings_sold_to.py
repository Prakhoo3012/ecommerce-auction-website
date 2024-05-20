# Generated by Django 4.1.7 on 2023-04-07 05:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0019_alter_bids_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="items",
            name="sold_to",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="new_owner",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="listings",
            name="sold_to",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="new_malik",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
