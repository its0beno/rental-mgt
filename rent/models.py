from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db.models import Sum
from decimal import Decimal
from dateutil.relativedelta import relativedelta as rel
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.
STATUS_CHOICES = [
    ("occupied", "OCCUPIED"),
    ("vacant", "VACANT"),
    ("under maintenance", "UNDER MAINTENANCE"),
    ("not for rent", "NOT FOR RENT"),
]

PAYMENT_METHOD_CHOICES = [
    ("cash", "CASH"),
    ("bank deposit", "BANK DEPOSIT"),
    ("check", "CHECK"),
]


class Building(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    address = models.CharField(_("Address"), max_length=150)
    img = models.ImageField(_("Building Image"), null= True, blank=True ,upload_to="img/")

    def __str__(self):
        return self.name


class Room(models.Model):
    building = models.ForeignKey("rent.Building", verbose_name=_(
        "Building"), on_delete=models.PROTECT)
    floor_no = models.PositiveIntegerField(_("Floor No."))
    room_type = models.ForeignKey("rent.RoomType", verbose_name=_(
        "Room Type"), on_delete=models.PROTECT)
    room_no = models.CharField(_("Room No."), max_length=10)
    width = models.DecimalField(
        _("Room Width"), max_digits=5, decimal_places=2, blank=True, null=True)
    length = models.DecimalField(
        _("Room Length"), max_digits=5, decimal_places=2, blank=True, null=True)
    area = models.DecimalField(_("Area"), max_digits=10, decimal_places=2)
    price_msq = models.DecimalField(
        _("Price per MSq"), max_digits=10, decimal_places=2)
    status = models.CharField(
        _("Status"), max_length=50, choices=STATUS_CHOICES, default="vacant")
    total_price = models.DecimalField(
        _("Total Price"), max_digits=10, decimal_places=2)
     
    room_img = models.ImageField(_("Room Image"), null=True, upload_to="img/", blank=True)

    # Tells if the object is active or not.
    is_active = models.BooleanField(default=True)

    # Fields that explains who and when the object is created.
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "Created By"), on_delete=models.PROTECT, related_name="created_by_room")
    created_date = models.DateTimeField(_("Created Date"), auto_now_add=True)

    # Fields that explains who and when the object is updated.
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "Updated By"), on_delete=models.PROTECT, related_name="updated_by_room")
    updated_date = models.DateTimeField(_("Updated Date"), auto_now=True)

    def save(self, *args, **kwargs):
        if self.width and self.length:
            self.area = self.width * self.length

        if self.area and self.price_msq:
            self.total_price = self.area * self.price_msq

        return super().save()

    def __str__(self) -> str:
        return self.room_no


class RoomType(models.Model):
    room_type = models.CharField(_("Room Type"), max_length=50)

    def __str__(self):
        return self.room_type


class Renter(models.Model):
    # Fields.
    first_name = models.CharField(_("First Name"), max_length=30)
    last_name = models.CharField(_("Last Name"), max_length=30)
    phone = models.IntegerField(_("Phone number"), )
    tin_no = models.IntegerField(_("Tin number"), )
    company_name = models.CharField(
        _("Company Name"), max_length=50,)
    deposited_amount = models.DecimalField(
        _("Deposited Amount"), max_digits=15, decimal_places=2, default=0)
    date_admitted = models.DateField(_("Date Admitted"), default=timezone.now)
    room = models.ForeignKey("rent.Room", verbose_name=_(
        "Room"), on_delete=models.PROTECT, related_name="rents")
    chat_id = models.IntegerField(_("Chat ID"),blank=True, null= True)
    license_img = models.ImageField(_("Company Licence"), upload_to="img/",null=True, blank=True)
    tin_img = models.ImageField(_("Tin Certificate"), upload_to="img/",null=True, blank=True)
    # Boolean that tells if the renter is renting.
    is_rented = models.BooleanField(_("Is Rented"), default=True)
    date_left = models.DateField(_("Date Field"), blank=True, null=True)

    # Fields that explains who and when the object  is created.
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "Created By"), on_delete=models.PROTECT, related_name="created_by_renter")
    created_date = models.DateTimeField(_("Created Date"), auto_now_add=True)

    # Fields that explains who and when the object is updated.
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "Updated By"), on_delete=models.PROTECT, related_name="updated_by_renter")
    updated_date = models.DateTimeField(_("Updated Date"), auto_now=True)

    def full_name(self) -> str:
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):

        if self.room and self.is_rented:
            if self.room.status == 'vacant':
                self.room.status = 'occupied'

        else:
            if self.room.status == "occupied":
                self.room.status = "vacant"

            self.date_left = timezone.now()

        self.room.save()

        return super().save()

    def __str__(self) -> str:
        return self.full_name() + f' -> {self.room}'


class Payment(models.Model):
    renter = models.ForeignKey("rent.Renter", verbose_name=_(
        "Renter"), on_delete=models.PROTECT)
    paid_date = models.DateField(_("Paid Date"), auto_now_add=True)
    no_of_months = models.PositiveIntegerField(_("No Of Months"))
    amount = models.DecimalField(
        _("Rent Cost"), max_digits=10, decimal_places=2)
    invoice_no = models.CharField(_("Invoice No"), max_length=50)
    slip_no = models.CharField(_("Slip No"), max_length=50)
    payment_method = models.CharField(
        _("Payment Method"), max_length=50, choices=PAYMENT_METHOD_CHOICES)
    remark = models.TextField(_("Remark"), blank=True, default="No Remark.")
    vat = models.DecimalField(_("VAT Amount"), max_digits=10, decimal_places=2)
    penality = models.DecimalField(
        _("Penality Amount"), max_digits=10, decimal_places=2, null=True , blank=True)

    # Reports
    report = models.ForeignKey("rent.Report", verbose_name=_(
        "Reported to."), on_delete=models.PROTECT, blank=True)

    # Fields that explains who and when the object is created.
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "Created By"), on_delete=models.PROTECT, related_name="created_by_payment")
    created_date = models.DateTimeField(_("Created Date"), auto_now_add=True)

    # Fields that explains who and when the object is updated.
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "Updated By"), on_delete=models.PROTECT, related_name="updated_by_payment")
    updated_date = models.DateTimeField(_("Updated Date"), auto_now=True)

    @property
    def new_paid(self):
        return self.amount + self.vat + self.penality

    def save(self):
        report = None
        try:
            report = Report.objects.get(renter=self.renter)
        except:
            pass
        if report:
            report.new_paid = self.amount + self.vat + self.penality
        else:
            report = Report()
            report.renter = self.renter
            report.total_paid = self.amount + self.vat + self.penality

        report.save()
        self.report = report

        super().save()

        report.save()
        return

    def __str__(self):
        return f'{self.renter} {self.created_date.month}'


class UserAdditionalInfo(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER, verbose_name=_("User"), on_delete=models.CASCADE)
    security_question = models.CharField(
        _("Sequrity Question"), max_length=50, default="")
    security_answer = models.CharField(
        _("Sequrity Answer"), max_length=50, default="")

    def __str__(self) -> str:
        return self.user.username


class Report(models.Model):
    renter = models.ForeignKey("rent.Renter", verbose_name=_(
        "Invoice No."), on_delete=models.CASCADE)
    payable_month = models.DecimalField(
        _("Payable Month"), max_digits=20, decimal_places=2, default=0)
    payable_amount = models.DecimalField(
        _("Payable Amount"), max_digits=10, decimal_places=2, default=0)
    total_paid = models.DecimalField(
        _("Total Paid"), max_digits=10, decimal_places=2, default=0, editable=False)

    def total_paid_calculator(self) -> Decimal:
        amount = self.payment_set.all().aggregate(Sum('amount'))
        vat = self.payment_set.all().aggregate(Sum('vat'))
        penality = self.payment_set.all().aggregate(Sum('penality'))

        if amount.get('amount__sum') is None:
            return Decimal(0)

        sum = amount.get('amount__sum') + vat.get('vat__sum') + \
            penality.get('penality__sum')

        total = sum + self.renter.deposited_amount

        return total

    @property
    def room_no(self) -> str:
        return self.renter.room.room_no

    @property
    def monthly_rate(self) -> float:
        return float(self.renter.room.total_price)

    @property
    def payable_months_value(self) -> float:
        date = rel(timezone.localtime().now(), self.renter.date_admitted)
        year = date.years
        months = date.months
        days = date.days

        total_months = (year*12)+(months)+(days/30)
        return round(total_months, 2)

    @property
    def payable_amount_value(self):
        return round(self.payable_months_value * self.monthly_rate, 2)

    @property
    def outstanding_balance(self):
        return round(self.payable_amount - self.total_paid, 2)

    @property
    def last_paid_date(self):
        queryset = self.payment_set.all().order_by("-created_date")
        if queryset:
            return queryset[0].paid_date
        else:
            return "Hasn't Paid Yet"

    @property
    def penality(self):
        if self.outstanding_balance < 0:
            # No penality
            return 0

        last_paid_date = self.last_paid_date
        if type(last_paid_date) == str:
            last_paid_date = self.renter.date_admitted

        number_of_days = rel(timezone.localtime().now(), last_paid_date)
        year = number_of_days.years
        months = number_of_days.months
        days = number_of_days.days

        total_days = ((year*12)+(months))*30 + days

        lookup_fields = models.Q(date_from__lte=total_days) & models.Q(
            date_to__gte=total_days)

        penality_query = Penality.objects.filter(lookup_fields)

        if not penality_query.exists():
            return 0

        penality = penality_query.first()

        penality_amount = (penality.penality_fee_percent /
                           100) * self.renter.room.total_price

        return round(penality_amount, 2)

    def save(self):
        self.payable_month = self.payable_months_value
        self.payable_amount = self.payable_amount_value
        self.total_paid = self.total_paid_calculator()

        return super().save()


class Penality(models.Model):
    date_from = models.PositiveIntegerField()
    date_to = models.PositiveIntegerField()
    penality_fee_percent = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.date_from} -> {self.date_to}"


class Vat(models.Model):
    vat_percent = models.DecimalField(
        _("Vat Pecentage"), max_digits=5, decimal_places=2, default=15)
