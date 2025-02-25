# Generated by Django 5.0.7 on 2024-08-08 19:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_alter_ticket_arrival_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='arrival_station',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='departure_station',
        ),
        migrations.RemoveField(
            model_name='train',
            name='arrival_station',
        ),
        migrations.RemoveField(
            model_name='train',
            name='departure_station',
        ),
        migrations.AddField(
            model_name='ticket',
            name='from_station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='from_ticket_station', to='tickets.station'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='to_station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_ticket_station', to='tickets.station'),
        ),
        migrations.AddField(
            model_name='train',
            name='station1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='station1', to='tickets.station'),
        ),
        migrations.AddField(
            model_name='train',
            name='station2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='station2', to='tickets.station'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='ticket_qr_codes/'),
        ),
        migrations.CreateModel(
            name='Trips',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_time', models.TimeField()),
                ('departure_time', models.TimeField()),
                ('from_station', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='from_station', to='tickets.station')),
                ('to_station', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_station', to='tickets.station')),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.train')),
            ],
        ),
        migrations.DeleteModel(
            name='TrainStations',
        ),
    ]
