# Generated by Django 4.2.1 on 2023-07-20 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lmsapp', '0025_rename_pickuppoint_package_pickuplocation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='package',
            old_name='pickUpLocation',
            new_name='recipientPickUpLocation',
        ),
    ]
