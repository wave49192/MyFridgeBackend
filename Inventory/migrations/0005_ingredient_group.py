# Generated by Django 5.0.3 on 2024-04-07 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0004_inventoryitem_quantity_inventoryitem_unit_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='group',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
