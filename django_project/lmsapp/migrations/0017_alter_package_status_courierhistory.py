# Generated by Django 4.2.1 on 2023-10-05 16:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lmsapp', '0016_rename_has_changed_password_user_has_set_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='status',
            field=models.CharField(choices=[('upcoming', 'Upcoming'), ('dropped_off', 'Dropped Off'), ('dispatched', 'Dispatched'), ('en_route', 'En Route'), ('warehouse_arrival', 'Warehouse Arrival'), ('in_house', 'In House'), ('in_transit', 'In Transit'), ('at_pickup', 'At Pickup'), ('ready_for_pickup', 'Ready for Pickup'), ('arrived', 'Arrived'), ('completed', 'Completed')], default='upcoming', max_length=20),
        ),
        migrations.CreateModel(
            name='CourierHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('upcoming', 'Upcoming'), ('dropped_off', 'Dropped Off'), ('dispatched', 'Dispatched'), ('en_route', 'En Route'), ('warehouse_arrival', 'Warehouse Arrival'), ('in_house', 'In House'), ('in_transit', 'In Transit'), ('at_pickup', 'At Pickup'), ('ready_for_pickup', 'Ready for Pickup'), ('arrived', 'Arrived'), ('completed', 'Completed')], max_length=20)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('courier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lmsapp.package')),
            ],
        ),
    ]
