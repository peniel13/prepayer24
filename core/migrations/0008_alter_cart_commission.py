# Generated by Django 5.1.3 on 2024-11-13 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_cart_commission_alter_cart_montant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='commission',
            field=models.DecimalField(blank=True, decimal_places=2, default=4000, max_digits=10, null=True),
        ),
    ]
