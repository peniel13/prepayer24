# Generated by Django 5.1.3 on 2024-11-13 13:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_payment2_station_prepay'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseClientStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('prenom', models.CharField(max_length=255)),
                ('postnom', models.CharField(max_length=255)),
                ('commune', models.CharField(max_length=255)),
                ('avenue', models.CharField(max_length=255)),
                ('numparcel', models.CharField(max_length=255)),
                ('identifiant', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('station_prepay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients', to='core.stationprepay')),
            ],
        ),
    ]
