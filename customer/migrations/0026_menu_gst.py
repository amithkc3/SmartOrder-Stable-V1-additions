# Generated by Django 2.0 on 2019-02-07 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0025_menu_itemname'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='gst',
            field=models.FloatField(default=0.7),
        ),
    ]