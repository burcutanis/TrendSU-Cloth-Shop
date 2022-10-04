# Generated by Django 4.0.4 on 2022-06-05 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0083_order_all_received'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='inTransit',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='processing',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
