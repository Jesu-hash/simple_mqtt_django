# Generated by Django 4.0.4 on 2022-05-22 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settingMqtt', '0002_settingmqtt_delete_settingconnection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settingmqtt',
            name='client_id',
            field=models.CharField(default='python-mqtt-53', editable=False, max_length=7),
        ),
    ]