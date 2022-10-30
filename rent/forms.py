from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import *


MONTHS_CHOICES = [
    (1, "January"),
    (2, "Febuaray"),
    (3, "March"),
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"),
    (11, "November"),
    (12, "December"),
]


class RegisterRoomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super(RegisterRoomForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    width = forms.DecimalField(
        min_value=0.00, decimal_places=2, required=False, label="Room Width")
    length = forms.DecimalField(
        min_value=0.00, decimal_places=2, required=False, label="Room Length")

    class Meta:
        model = Room
        fields = [
            "building",
            "floor_no",
            "room_type",
            "room_no",
            "width",
            "length",
            "price_msq",
            "status"
        ]


class RegisterRenterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        super(RegisterRenterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        if not kwargs["instance"]:
            self.fields['room'].queryset = Room.objects.filter(status="vacant")
        else:
            self.fields["room"].queryset = Room.objects.exclude(
                status="under maintenance").exclude(status='not for rent')

    class Meta:
        model = Renter
        fields = [
            "first_name",
            "last_name",
            "phone",
            "company_name",
            "tin_no",
            "room",
            "chat_id",
            "deposited_amount",
            "date_admitted"
        ]

    def clean_room(self):
        old_room = None
        try:
            old_room = Room.objects.get(
                id=self.get_initial_for_field(self.fields['room'], 'room'))
        except:
            pass

        new_room = self.cleaned_data['room']
        if old_room and new_room != old_room:
            if not new_room.rents.filter(is_rented=False) or new_room.status == 'occupied':
                raise forms.ValidationError(
                    "Room is occupied"
                )

        return new_room

    def save(self):
        room = None
        try:
            room = Room.objects.get(
                id=self.get_initial_for_field(self.fields['room'], 'room'))
        except Room.DoesNotExist:
            pass
        new_room = self.cleaned_data['room']
        if room:
            if room.status == "occupied":
                room.status = "vacant"
                room.save()
        return super().save()


class RegisterPaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super(RegisterPaymentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Payment
        fields = [
            "renter",
            "no_of_months",
            "amount",
            "vat",
            "penality",
            "invoice_no",
            "slip_no",
            "payment_method",
            "remark",

        ]


class RegisterRoomTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegisterRoomTypeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = RoomType
        fields = ["room_type"]


class UserRegistrationForm(UserCreationForm):

    security_question = forms.CharField(
        label="Security Question", max_length=100, required=False)
    security_answer = forms.CharField(
        label="Security Answer", max_length=100, required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "groups")
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            user.groups.add(*self.cleaned_data['groups'])
            user.save()
            user_additional_info = UserAdditionalInfo(
                security_question=self.cleaned_data["security_question"], security_answer=self.cleaned_data['security_answer'], user=user)
            user_additional_info.save()

        return user


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "groups")
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.groups.add(*self.cleaned_data['groups'])
            user.save()

        return user


class UserAdditionalInfoForm(forms.ModelForm):
    class Meta:
        model = UserAdditionalInfo
        fields = [
            "security_question",
            "security_answer",
        ]


class RenterLeavesRoomForm(forms.ModelForm):
    class Meta:
        model = Renter
        fields = ['is_rented']


class UpdateRenterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        super(UpdateRenterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        if not kwargs["instance"]:
            self.fields['room'].queryset = Room.objects.filter(status="vacant")
        else:
            self.fields["room"].queryset = Room.objects.exclude(
                status="under maintenance").exclude(status='not for rent')

    class Meta:
        model = Renter
        fields = [
            "first_name",
            "last_name",
            "phone",
            "room",
            "chat_id",
            "deposited_amount",
            "date_admitted",
            "is_rented"
        ]

    def clean_room(self):
        old_room = None
        try:
            old_room = Room.objects.get(
                id=self.get_initial_for_field(self.fields['room'], 'room'))
        except:
            pass

        new_room = self.cleaned_data['room']
        if old_room and new_room != old_room:
            if not new_room.rents.filter(is_rented=False) or new_room.status == 'occupied':
                raise forms.ValidationError(
                    "Room is occupied"
                )

        return new_room

    def save(self):
        room = None
        try:
            room = Room.objects.get(
                id=self.get_initial_for_field(self.fields['room'], 'room'))
        except Room.DoesNotExist:
            pass
        if room:
            if room.status == "occupied":
                room.status = "vacant"
                room.save()
        return super().save()


class RegisterBuildingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegisterBuildingForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Building
        fields = [
            "name",
            "address",
        ]


class RegisterPenalityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegisterPenalityForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Penality
        fields = [
            "date_from",
            "date_to",
            "penality_fee_percent",
        ]


class RegisterVatForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegisterVatForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Vat
        fields = [
            "vat_percent",
        ]
