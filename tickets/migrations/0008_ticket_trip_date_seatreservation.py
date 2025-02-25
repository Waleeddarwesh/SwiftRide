# Generated by Django 5.0.7 on 2024-08-13 19:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0007_train_current_latitude_train_current_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='trip_date',
            field=models.DateField(default=None),
        ),
        migrations.CreateModel(
            name='SeatReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reserved', models.BooleanField(default=True)),
                ('reservation_number', models.IntegerField()),
                ('reservation_date', models.DateField()),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.seat')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.trips')),
            ],
            options={
                'unique_together': {('trip', 'seat', 'reservation_number', 'reservation_date')},
            },
        ),
    ]
