# Generated by Django 3.2.9 on 2022-03-18 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0011_auto_20220318_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renter',
            name='room',
            field=models.ForeignKey(default=555, on_delete=django.db.models.deletion.CASCADE, related_name='rents', to='rent.room', verbose_name='Room'),
            preserve_default=False,
        ),
    ]
