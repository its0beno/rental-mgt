# Generated by Django 3.2 on 2022-05-05 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0019_alter_room_room_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='Penatliy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.PositiveIntegerField()),
                ('date_to', models.PositiveIntegerField()),
                ('penality_fee_percent', models.DecimalField(decimal_places=2, max_digits=3)),
            ],
        ),
    ]
