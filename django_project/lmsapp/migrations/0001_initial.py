# Generated by Django 4.2.1 on 2023-08-10 12:54

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import lmsapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=40)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('courier', 'Courier'), ('sender', 'Sender'), ('drop_pick_zone', 'Drop/Pick Zone'), ('warehouse', 'Warehouse')], max_length=20, verbose_name='Role')),
                ('status', models.CharField(choices=[('available', 'Available'), ('on-trip', 'On Trip')], default='available', max_length=20)),
                ('verification_token', models.CharField(blank=True, max_length=200, null=True)),
                ('tag', models.CharField(blank=True, max_length=20, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', lmsapp.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='DropPickZone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('address', models.CharField(max_length=40)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('tag', models.CharField(blank=True, max_length=20, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='drop_pick_zones_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='drop_pick_zones_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('address', models.CharField(max_length=40)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('tag', models.CharField(blank=True, max_length=20, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='warehouse_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='warehouse_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('packageName', models.CharField(max_length=100)),
                ('deliveryType', models.CharField(choices=[('standard', 'Standard'), ('premium', 'Premium'), ('express', 'Express')], max_length=20)),
                ('packageDescription', models.TextField()),
                ('recipientName', models.CharField(max_length=100)),
                ('recipientEmail', models.CharField(max_length=100)),
                ('recipientTelephone', models.CharField(max_length=100)),
                ('recipientAddress', models.CharField(max_length=200)),
                ('recipientIdentification', models.CharField(max_length=200)),
                ('sendersName', models.CharField(max_length=200)),
                ('sendersEmail', models.CharField(max_length=200)),
                ('sendersAddress', models.CharField(blank=True, max_length=200, null=True)),
                ('sendersContact', models.CharField(max_length=200)),
                ('sender_latitude', models.FloatField(blank=True, null=True)),
                ('sender_longitude', models.FloatField(blank=True, null=True)),
                ('recipient_latitude', models.FloatField(blank=True, null=True)),
                ('recipient_longitude', models.FloatField(blank=True, null=True)),
                ('deliveryFee', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('genderType', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=20, verbose_name='Gender')),
                ('package_number', models.CharField(max_length=50, unique=True)),
                ('status', models.CharField(choices=[('upcoming', 'Upcoming'), ('dropped_off', 'Dropped Off'), ('dispatched', 'Dispatched'), ('en_route', 'En Route'), ('warehouse_arrival', 'Warehouse Arrival'), ('in_house', 'In House'), ('in_transit', 'In Transit'), ('at_pickup', 'At Pickup'), ('ready_for_pickup', 'Ready for Pickup'), ('pending_delivery', 'Pending Delivery'), ('out_for_delivery', 'Out for Delivery'), ('ongoing', 'Ongoing'), ('arrived', 'Arrived'), ('completed', 'Completed')], default='upcoming', max_length=20)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('received_at', models.DateTimeField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('in_house_at', models.DateTimeField(blank=True, null=True)),
                ('dispatched_at', models.DateTimeField(blank=True, null=True)),
                ('assigned_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('otp', models.CharField(blank=True, max_length=6, null=True)),
                ('courier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_packages', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='packages_created_by', to=settings.AUTH_USER_MODEL)),
                ('dropOffLocation', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='packages_dropped_off', to='lmsapp.droppickzone')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='packages_modified_by', to=settings.AUTH_USER_MODEL)),
                ('recipientPickUpLocation', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='packages_picked_up', to='lmsapp.droppickzone')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='packages', to=settings.AUTH_USER_MODEL)),
                ('warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='packages_in_house', to='lmsapp.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='droppickzone',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='drop_pick_zones', to='lmsapp.warehouse'),
        ),
        migrations.AddField(
            model_name='user',
            name='drop_pick_zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='users', to='lmsapp.droppickzone'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='modified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='user',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='users', to='lmsapp.warehouse'),
        ),
    ]
