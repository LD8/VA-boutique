# Generated by Django 3.0.2 on 2020-02-28 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0014_auto_20200223_1647'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='anonymousorder',
            options={'ordering': ['-active', '-date_ordered'], 'verbose_name': 'Anonymous Order', 'verbose_name_plural': 'Anonymous Orders'},
        ),
    ]
