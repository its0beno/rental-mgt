# Generated by Django 4.0.5 on 2022-10-30 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='renter',
            name='id_no',
        ),
        migrations.AddField(
            model_name='renter',
            name='company_name',
            field=models.CharField(default='kurtu', max_length=50, verbose_name='Compane Name'),
        ),
        migrations.AddField(
            model_name='renter',
            name='tin_no',
            field=models.CharField(default=0, max_length=30, verbose_name='Tin number'),
        ),
    ]