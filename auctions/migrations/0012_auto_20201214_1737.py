# Generated by Django 3.1 on 2020-12-14 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20201125_1748'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bid',
            options={'get_latest_by': 'price'},
        ),
    ]