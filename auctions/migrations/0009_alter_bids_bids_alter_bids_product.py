# Generated by Django 4.1.7 on 2023-04-04 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0008_alter_listings_image_watchlist_bids"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bids",
            name="bids",
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name="bids",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="saman",
                to="auctions.listings",
            ),
        ),
    ]
