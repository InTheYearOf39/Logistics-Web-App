# Generated by Django 4.2.1 on 2023-09-04 09:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lmsapp', '0011_alter_user_warehouse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='droppickzone',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='drop_pick_zones_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='droppickzone',
            name='modified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='drop_pick_zones_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='package',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='packages_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='package',
            name='dropOffLocation',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='packages_dropped_off', to='lmsapp.droppickzone'),
        ),
        migrations.AlterField(
            model_name='package',
            name='modified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='packages_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='package',
            name='recipientPickUpLocation',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='packages_picked_up', to='lmsapp.droppickzone'),
        ),
        migrations.AlterField(
            model_name='package',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='packages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='package',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='packages_in_house', to='lmsapp.warehouse'),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='drop_pick_zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='lmsapp.droppickzone'),
        ),
        migrations.AlterField(
            model_name='user',
            name='modified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='warehouse_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='modified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='warehouse_modified_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
