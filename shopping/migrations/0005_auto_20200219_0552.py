# Generated by Django 3.0.2 on 2020-02-19 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0004_auto_20200219_0552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anonymousorder',
            name='ref_number',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]