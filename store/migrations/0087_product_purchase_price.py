# Generated by Django 4.0.4 on 2022-06-06 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0086_order_delivered'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='purchase_price',
            field=models.IntegerField(default=50),
        ),
    ]
