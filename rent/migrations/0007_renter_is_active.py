# Generated by Django 3.2.9 on 2022-03-16 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0006_alter_payment_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='renter',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is Active'),
        ),
    ]