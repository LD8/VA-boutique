# Generated by Django 3.0.2 on 2020-02-23 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_slug'),
        ('shopping', '0012_auto_20200223_0509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='date_ordered',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='is_ordered',
        ),
        migrations.AddField(
            model_name='order',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.Profile'),
            preserve_default=False,
        ),
    ]
