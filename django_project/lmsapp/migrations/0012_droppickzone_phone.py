# Generated by Django 4.2.1 on 2023-07-05 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmsapp', '0011_warehouse_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='droppickzone',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
