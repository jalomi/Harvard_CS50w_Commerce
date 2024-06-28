# Generated by Django 5.0.6 on 2024-06-28 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_bid_bidder_bid_listing_bid_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='wins',
            field=models.ManyToManyField(blank=True, related_name='auction_wins', to='auctions.listing'),
        ),
    ]
