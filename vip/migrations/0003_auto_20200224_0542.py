# Generated by Django 3.0.2 on 2020-02-24 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vip', '0002_auto_20200223_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viporder',
            name='item_image2',
            field=models.ImageField(blank=True, null=True, upload_to='vip_order', verbose_name='Upload another photo of the item (optional)'),
        ),
        migrations.AlterField(
            model_name='viporder',
            name='item_image3',
            field=models.ImageField(blank=True, null=True, upload_to='vip_order', verbose_name='Upload another photo of the item (optional)'),
        ),
    ]