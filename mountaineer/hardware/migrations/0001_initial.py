# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-10 18:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields
import mountaineer.hardware
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('rack_units', models.PositiveIntegerField(help_text='Height of rack in Rack Units')),
                ('posts', models.PositiveIntegerField(help_text='Number of posts in the rack (usually 2 or 4)')),
            ],
        ),
        migrations.CreateModel(
            name='CabinetAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(blank=True, null=True)),
                ('orientation', enumfields.fields.EnumIntegerField(blank=True, enum=mountaineer.hardware.RackOrientation, null=True)),
                ('depth', enumfields.fields.EnumIntegerField(blank=True, enum=mountaineer.hardware.RackDepth, null=True)),
                ('cabinet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hardware.Cabinet')),
            ],
        ),
        migrations.CreateModel(
            name='Datacenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('vendor', models.CharField(max_length=256)),
                ('address', models.CharField(max_length=256)),
                ('noc_phone', models.CharField(blank=True, max_length=24)),
                ('noc_email', models.EmailField(blank=True, max_length=254)),
                ('noc_url', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_id', models.PositiveIntegerField(blank=True, help_text='ID in external asset database, if any.', unique=True)),
                ('asset_tag', models.CharField(blank=True, help_text='Asset tag, if any.', max_length=128, unique=True)),
                ('description', models.CharField(max_length=256)),
                ('manufacturer', models.CharField(blank=True, max_length=128)),
                ('model', models.CharField(blank=True, max_length=128)),
                ('serial', models.CharField(blank=True, max_length=256)),
                ('rack_units', models.IntegerField(blank=True, null=True)),
                ('name', models.SlugField()),
                ('ports', models.PositiveIntegerField(help_text='Number of ports available on the device')),
                ('speed', enumfields.fields.EnumIntegerField(enum=mountaineer.hardware.SwitchSpeed)),
                ('interconnect', enumfields.fields.EnumIntegerField(enum=mountaineer.hardware.SwitchInterconnect)),
                ('device', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hardware.Device')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PortAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_port', models.PositiveIntegerField()),
                ('connected_device', models.ForeignKey(help_text='The device being connected.', on_delete=django.db.models.deletion.CASCADE, related_name='connected_device', to='hardware.Device')),
                ('device', models.ForeignKey(help_text='The device (e.g. switch or pdu) being connected to.', on_delete=django.db.models.deletion.CASCADE, to='hardware.Device')),
            ],
        ),
        migrations.CreateModel(
            name='PowerDistributionUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_id', models.PositiveIntegerField(blank=True, help_text='ID in external asset database, if any.', unique=True)),
                ('asset_tag', models.CharField(blank=True, help_text='Asset tag, if any.', max_length=128, unique=True)),
                ('description', models.CharField(max_length=256)),
                ('manufacturer', models.CharField(blank=True, max_length=128)),
                ('model', models.CharField(blank=True, max_length=128)),
                ('serial', models.CharField(blank=True, max_length=256)),
                ('rack_units', models.IntegerField(blank=True, null=True)),
                ('name', models.SlugField()),
                ('ports', models.PositiveIntegerField(help_text='Number of ports available on the device')),
                ('volts', models.PositiveIntegerField()),
                ('amps', models.PositiveIntegerField()),
                ('device', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hardware.Device')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_id', models.PositiveIntegerField(blank=True, help_text='ID in external asset database, if any.', unique=True)),
                ('asset_tag', models.CharField(blank=True, help_text='Asset tag, if any.', max_length=128, unique=True)),
                ('description', models.CharField(max_length=256)),
                ('manufacturer', models.CharField(blank=True, max_length=128)),
                ('model', models.CharField(blank=True, max_length=128)),
                ('serial', models.CharField(blank=True, max_length=256)),
                ('rack_units', models.IntegerField(blank=True, null=True)),
                ('cpu_count', models.PositiveIntegerField(blank=True, help_text='Number of physical, socketed CPUs (not cores or threads)', null=True)),
                ('cpu_manufacturer', enumfields.fields.EnumIntegerField(blank=True, enum=mountaineer.hardware.CpuManufacturer, null=True)),
                ('cpu_model', models.CharField(blank=True, max_length=128)),
                ('device', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hardware.Device')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='cabinetassignment',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hardware.Device'),
        ),
        migrations.AddField(
            model_name='cabinet',
            name='datacenter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hardware.Datacenter'),
        ),
    ]