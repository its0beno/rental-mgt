# Generated by Django 4.0.3 on 2022-03-21 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0015_renter_date_left'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='renter',
            name='is_active',
        ),
    ]
