# Generated by Django 4.0.5 on 2022-07-08 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0028_rename_penality_payment_penality'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=2, max_digits=10, verbose_name='Penality Amount'),
            preserve_default=False,
        ),
    ]