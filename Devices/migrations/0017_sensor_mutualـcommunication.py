# Generated by Django 4.0.5 on 2022-08-25 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Devices', '0016_sensorfordevice_sampleduration'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='mutualـcommunication',
            field=models.BooleanField(default=False),
        ),
    ]
