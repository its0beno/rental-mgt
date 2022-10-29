# Generated by Django 4.0.5 on 2022-10-22 15:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('address', models.CharField(max_length=150, verbose_name='Address')),
            ],
        ),
        migrations.CreateModel(
            name='Penality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.PositiveIntegerField()),
                ('date_to', models.PositiveIntegerField()),
                ('penality_fee_percent', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Renter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=30, verbose_name='Last Name')),
                ('phone', models.CharField(max_length=30, verbose_name='Phone number')),
                ('id_no', models.CharField(max_length=50, verbose_name='ID No.')),
                ('deposited_amount', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Deposited Amount')),
                ('date_admitted', models.DateField(default=django.utils.timezone.now, verbose_name='Date Admitted')),
                ('chat_id', models.CharField(default=0, max_length=50, verbose_name='Chat ID')),
                ('is_rented', models.BooleanField(default=True, verbose_name='Is Rented')),
                ('date_left', models.DateField(blank=True, null=True, verbose_name='Date Field')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_by_renter', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(max_length=50, verbose_name='Room Type')),
            ],
        ),
        migrations.CreateModel(
            name='Vat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vat_percent', models.DecimalField(decimal_places=2, default=15, max_digits=5, verbose_name='Vat Pecentage')),
            ],
        ),
        migrations.CreateModel(
            name='UserAdditionalInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('security_question', models.CharField(default='', max_length=50, verbose_name='Sequrity Question')),
                ('security_answer', models.CharField(default='', max_length=50, verbose_name='Sequrity Answer')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor_no', models.PositiveIntegerField(verbose_name='Floor No.')),
                ('room_no', models.CharField(max_length=10, verbose_name='Room No.')),
                ('width', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Room Width')),
                ('length', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Room Length')),
                ('area', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Area')),
                ('price_msq', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price per MSq')),
                ('status', models.CharField(choices=[('occupied', 'OCCUPIED'), ('vacant', 'VACANT'), ('under maintenance', 'UNDER MAINTENANCE'), ('not for rent', 'NOT FOR RENT')], default='vacant', max_length=50, verbose_name='Status')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total Price')),
                ('is_active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rent.building', verbose_name='Building')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_by_room', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rent.roomtype', verbose_name='Room Type')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='updated_by_room', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payable_month', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Payable Month')),
                ('payable_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Payable Amount')),
                ('total_paid', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10, verbose_name='Total Paid')),
                ('renter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rent.renter', verbose_name='Invoice No.')),
            ],
        ),
        migrations.AddField(
            model_name='renter',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rents', to='rent.room', verbose_name='Room'),
        ),
        migrations.AddField(
            model_name='renter',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='updated_by_renter', to=settings.AUTH_USER_MODEL, verbose_name='Updated By'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_date', models.DateField(auto_now_add=True, verbose_name='Paid Date')),
                ('no_of_months', models.PositiveIntegerField(verbose_name='No Of Months')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Rent Cost')),
                ('invoice_no', models.CharField(max_length=50, verbose_name='Invoice No')),
                ('slip_no', models.CharField(max_length=50, verbose_name='Slip No')),
                ('payment_method', models.CharField(choices=[('cash', 'CASH'), ('bank deposit', 'BANK DEPOSIT'), ('check', 'CHECK')], max_length=50, verbose_name='Payment Method')),
                ('remark', models.TextField(blank=True, default='No Remark.', verbose_name='Remark')),
                ('vat', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='VAT Amount')),
                ('penality', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Penality Amount')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_by_payment', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('renter', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rent.renter', verbose_name='Renter')),
                ('report', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='rent.report', verbose_name='Reported to.')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='updated_by_payment', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
        ),
    ]
