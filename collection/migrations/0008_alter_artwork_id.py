# Generated by Django 4.2.6 on 2023-11-07 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0007_alter_artwork_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]