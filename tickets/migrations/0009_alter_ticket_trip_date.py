# Generated by Django 5.0.7 on 2024-08-13 19:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0008_ticket_trip_date_seatreservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='trip_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
