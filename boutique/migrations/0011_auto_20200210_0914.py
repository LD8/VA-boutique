# Generated by Django 3.0.2 on 2020-02-10 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boutique', '0010_auto_20200210_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tag_discount_percentage',
            field=models.IntegerField(default=0),
        ),
    ]
