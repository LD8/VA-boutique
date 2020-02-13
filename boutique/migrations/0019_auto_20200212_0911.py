# Generated by Django 3.0.2 on 2020-02-12 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boutique', '0018_item_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='brand',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, to='boutique.Brand'),
        ),
    ]
