# Generated by Django 4.0.4 on 2022-05-07 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0038_payment_order_payment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='item',
            new_name='product',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='subtotal',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
