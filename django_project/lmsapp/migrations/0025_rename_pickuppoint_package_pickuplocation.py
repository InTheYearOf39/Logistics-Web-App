# Generated by Django 4.2.1 on 2023-07-19 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lmsapp', '0024_package_pickuppoint'),
    ]

    operations = [
        migrations.RenameField(
            model_name='package',
            old_name='pickupPoint',
            new_name='pickUpLocation',
        ),
    ]
