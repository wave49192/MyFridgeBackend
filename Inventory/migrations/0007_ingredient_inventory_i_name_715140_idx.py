# Generated by Django 5.0.3 on 2024-04-08 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0006_rename_ingredients_inventory_items'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='ingredient',
            index=models.Index(fields=['name'], name='Inventory_i_name_715140_idx'),
        ),
    ]