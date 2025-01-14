# Generated by Django 5.1.3 on 2024-11-11 22:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_stationprepay_payment_paymentconfirmation_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(help_text='Numéro de paiement associé à cette station', max_length=20, unique=True)),
                ('image', models.ImageField(blank=True, help_text='Image associée au numéro de paiement', null=True, upload_to='payment_numbers/')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_numbers', to='core.stationprepay')),
            ],
        ),
    ]
