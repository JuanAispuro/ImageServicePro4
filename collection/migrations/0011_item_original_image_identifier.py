# Generated by Django 4.2.6 on 2023-11-30 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0010_rename_image_item_imageoriginal_item_imageprocessed1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='original_image_identifier',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]