# Generated by Django 3.0.2 on 2020-02-03 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boutique', '0010_auto_20200203_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='boutique.SubCategory'),
        ),
    ]
