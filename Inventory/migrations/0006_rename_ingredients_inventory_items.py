# Generated by Django 5.0.3 on 2024-04-07 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0005_ingredient_group'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventory',
            old_name='ingredients',
            new_name='items',
        ),
    ]
