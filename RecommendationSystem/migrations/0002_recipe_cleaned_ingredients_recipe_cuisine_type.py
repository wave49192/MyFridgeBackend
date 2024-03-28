# Generated by Django 5.0.3 on 2024-03-28 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RecommendationSystem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='cleaned_ingredients',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='cuisine_type',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
