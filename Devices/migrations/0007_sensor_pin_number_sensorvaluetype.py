# Generated by Django 4.0.5 on 2022-07-01 14:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Devices', '0006_alter_sensorfordevice_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='pin_number',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.CreateModel(
            name='SensorValueType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('types', models.CharField(choices=[('INT', 'integer'), ('STR', 'string')], default=1, max_length=4)),
                ('validation', models.JSONField()),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensor', to='Devices.sensor')),
            ],
            options={
                'unique_together': {('sensor', 'name')},
            },
        ),
    ]
