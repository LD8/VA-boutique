# Generated by Django 3.0.2 on 2020-02-28 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_profile_city'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
    ]