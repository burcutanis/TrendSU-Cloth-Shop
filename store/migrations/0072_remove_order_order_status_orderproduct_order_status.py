# Generated by Django 4.0.4 on 2022-05-15 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0071_order_distributor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_status',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='order_status',
            field=models.CharField(blank=True, choices=[('Order Received', 'Order Received'), ('Order Processing', 'Order Processing'), ('Order in transit', 'Order in transit'), ('Order delivered', 'Order Delivered')], max_length=50, null=True),
        ),
    ]
