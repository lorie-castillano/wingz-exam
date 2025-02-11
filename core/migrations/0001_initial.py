# Generated by Django 5.1.5 on 2025-01-31 01:48

import django.contrib.auth.models
import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id_user', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(blank=True, choices=[('admin', 'admin'), ('driver', 'driver'), ('rider', 'rider')], default='admin', max_length=10, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('username', models.CharField(blank=True, max_length=50, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id_ride', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(blank=True, choices=[('en-route', 'en-route'), ('pickup', 'pickup'), ('dropoff', 'dropoff')], default='en-route', max_length=10, null=True)),
                ('pickup_latitude', models.FloatField()),
                ('pickup_longitude', models.FloatField()),
                ('dropoff_latitude', models.FloatField()),
                ('dropoff_longitude', models.FloatField()),
                ('pickup_time', models.DateTimeField(blank=True, null=True)),
                ('pickup_location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('id_driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_driver', to=settings.AUTH_USER_MODEL)),
                ('id_rider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(class)s_rider', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RideEvent',
            fields=[
                ('id_ride_event', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField()),
                ('id_ride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ride')),
            ],
        ),
    ]
