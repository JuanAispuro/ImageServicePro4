# Generated by Django 4.2.6 on 2023-11-06 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='path',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='title',
            field=models.CharField(max_length=500),
        ),
    ]