# Generated by Django 4.0.4 on 2022-05-12 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0060_alter_product_distributor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='distributor',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]
