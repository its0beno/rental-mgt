# Generated by Django 4.0.5 on 2022-07-03 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0023_vat_delete_penaliypaymenthistory_payment_vat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='vat',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='VAT Amount'),
        ),
    ]
