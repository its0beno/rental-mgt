from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from .forms import *
from .mixins import *


# Create your views here.

def permissions(request):
    context ={
        'room_permission': request.user.has_perm(perm="rent.view_room"),
        'renter_permission': request.user.has_perm(perm="rent.view_renter"),
        'report_permission': request.user.has_perm(perm="rent.view_report"),
        'payment_permission': request.user.has_perm(perm="rent.view_payment"),
        'user_permission': request.user.has_perm(perm="auth.view_user"),  
        'roomtype_permission': request.user.has_perm(perm="auth.view_roomtype"),
    }

    return context


@login_required
def dashboard_page(request):
    rooms = Room.objects.all()
    renters = Renter.objects.all()
    payments = Payment.objects.all()
    rooms_rented_this_month = renters.filter(is_rented=True).filter(updated_date__year = timezone.now().year, updated_date__month = timezone.now().month).count()
    amount_collected_this_month = payments.filter(paid_date__year = timezone.now().year, paid_date__month = timezone.now().month).aggregate(Sum('amount')).get("amount__sum")
    this_year_balance = payments.filter(updated_date__year = timezone.now().year).aggregate(Sum('amount')).get("amount__sum")
    # Over Due Payments
    free_rooms = Room.objects.filter(status = "vacant").count()
    used_rooms = Room.objects.filter(status = "occupied").count()

    context = {
        "rooms": rooms,
        "renters": renters,
        "payments": payments,
        "rooms_rented_this_month": rooms_rented_this_month,
        "amount_collected_this_month": amount_collected_this_month,
        "this_year_balance": this_year_balance,
        # "over_due_payments": over_due_payments,
        "free_rooms": free_rooms,
        "title": "Dashboard",
        "tab_name": "Dashboard",
        "open": "dashboard",
        "card-header": "Dashboard",
        "used_rooms" : used_rooms,
        **permissions(request)
    }

    return render(request, 'rent/dashboard.html', context)



class RoomCreateView(LoginRequiredMixin, RoomCreatePermissionMixin, CreateView):
    form_class = RegisterRoomForm
    success_url = reverse_lazy('list-rooms')
    context_object_name = 'form'
    template_name = 'rent/register-room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tab_name"] = "Register"
        context["title"] = "Room"
        context["card_header"] = "Register Room"
        context["open"] = "room"

        return {**context, **permissions(self.request)}

    def form_valid(self, form):
        messages.success(self.request, 'Room Registered Successfully')
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        form.instance.status = "vacant"


        return super().form_valid(form)


class RoomListView(LoginRequiredMixin, RoomViewPermissionMixin, ListView):
    model = Room
    template_name = "rent/list.html"
    filter=None

    def get(self, *args, **kwargs):
        self.filter = kwargs.get("filter",None)
        return super().get(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Room"
        context["open"] = "room"
        context['obj_model'] = "room"
        
        
        return {**context, **permissions(self.request)}

    def get_queryset(self):
        rooms = Room.objects.filter(is_active=True)
        if self.filter:
            rooms = Room.objects.filter(is_active=True).filter(status= self.filter)
            
        return rooms
    

class RoomDetailView(LoginRequiredMixin, RoomViewPermissionMixin, DetailView):
    model = Room
    login_required = True
    template_name = "rent/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Room"
        context["open"] = "room"

        return {**context, **permissions(self.request)}


class RoomUpdateView(LoginRequiredMixin, RoomUpdatePermissionMixin, UpdateView):
    login_required = True
    model = Room
    form_class = RegisterRoomForm
    context_object_name = "form"
    success_url = reverse_lazy("list-rooms")
    template_name = "rent/register-room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Room"
        context["card_header"] = "Update Room"
        context["open"] = "room"


        return {**context, **permissions(self.request)}


    def form_valid(self, form):
        messages.success(self.request, 'Room Updated Successfully')
        form.instance.updated_by = self.request.user


        return super().form_valid(form)




class RenterCreateView(CreateView, LoginRequiredMixin, RenterCreatePermissionMixin):
    form_class = RegisterRenterForm
    context_object_name = 'form'
    template_name = 'rent/register.html'
    success_url = reverse_lazy('list-renters')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tab_name"] = "Register"
        context["title"] = "Renter"
        context["card_header"] = "Register Renter"
        context["open"] = "renter"

        return {**context, **permissions(self.request)}

    def form_valid(self, form):
        messages.success(self.request, 'Renter Registered Successfully')
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)



class RenterListView(LoginRequiredMixin, RenterViewPermissionMixin, ListView):
    model = Renter
    template_name = "rent/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Renter"
        context["open"] = "renter"
        context['obj_model'] = "renter"

        return {**context, **permissions(self.request)}

    def get_queryset(self):
        return Renter.objects.filter(is_active=True)
    



class RenterDetailView(LoginRequiredMixin, RenterCreatePermissionMixin, DetailView):
    model = Renter
    login_required = True
    template_name = "rent/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Renters"
        context["open"] = "renter"
        context['obj_model'] = "renter"

        return {**context, **permissions(self.request)}



class RenterUpdateView(LoginRequiredMixin, RenterUpdatePermissionMixin, UpdateView):
    login_required = True
    model = Renter
    form_class = UpdateRenterForm
    context_object_name = "form"
    success_url = reverse_lazy("list-renters")
    template_name = "rent/register.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Renter"
        context["card_header"] = "Update Renter"
        context["open"] = "renter"
        
        return {**context, **permissions(self.request)}


    def form_valid(self, form):
        messages.success(self.request, 'Renter Updated Successfully')
        form.instance.updated_by = self.request.user


        return super().form_valid(form)


class PaymentCreateView(LoginRequiredMixin, PaymentCreatePermissionMixin, CreateView):
    form_class = RegisterPaymentForm
    success_url = reverse_lazy('list-payments')
    context_object_name = 'form'
    template_name = 'rent/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tab_name"] = "Register"
        context["title"] = "Payment"
        context["card_header"] = "Register Payment"
        context["open"] = "payment"

        return {**context, **permissions(self.request)}


    def form_valid(self, form):
        messages.success(self.request, 'Payment Registered Successfully')
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user


        return super().form_valid(form)


class PaymentUpdateView(LoginRequiredMixin, PaymentUpdatePermissionMixin, UpdateView):
    login_required = True
    model = Payment
    form_class = RegisterPaymentForm
    context_object_name = "form"
    success_url = reverse_lazy("list-payments")
    template_name = "rent/register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Payment"
        context["card_header"] = "Update Payment"
        context["open"] = "payment"
        
        return {**context, **permissions(self.request)}
    
    
    def form_valid(self, form):
        messages.success(self.request, 'Payment Updated Successfully')
        form.instance.updated_by = self.request.user


        return super().form_valid(form)




class PaymentListView(LoginRequiredMixin, PaymentViewPermissionMixin, ListView):
    model = Payment
    template_name = "rent/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Payment"
        context["open"] = "payment"
        context['obj_model'] = "payment"

        return {**context, **permissions(self.request)}

class PaymentDetailView(LoginRequiredMixin, PaymentViewPermissionMixin, DetailView):
    model = Payment
    login_required = True
    template_name = "rent/detail-payment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Payments"
        context["open"] = "payment"
        context['obj_model'] = "renter"

        return {**context, **permissions(self.request)}


@login_required
@permission_required(perm="rent.delete_renter")
def RenterDeleteView(request, pk):
    object = Renter.objects.get(id= pk)
    if request.method== "POST":
        object.is_active=False
        object.save()

        room = object.room
        if room.status=="occupied":
            room.status = "vacant"
            room.save()

        messages.success(request, message="Renter Deleted Sucessfully")
        
        return redirect("list-renters")

    context={
        "title": "Renter",
        "open": "renter",
        "obj_model": "renter",
        "object": object,
        **permissions(request)
    }

    return render(request, "rent/delete_page.html", context)


@login_required
@permission_required(perm="rent.delete_room")
def RoomDeleteView(request, pk):
    object = Room.objects.get(id= pk)
    if request.method== "POST":
        renter = object.rents.filter(is_rented=True)[0]
        renter.is_rented= False
        object.is_active=False
        object.save()
        renter.save()

        messages.success(request, message="Room Deleted Sucessfully")
        
        return redirect("list-rooms")

    context={
        "title": "Room",
        "open": "room",
        "obj_model": "room",
        "object":object,
        **permissions(request)
    }

    return render(request, "rent/delete_page.html", context)


@login_required
@permission_required(perm="rent.view_report")
def ReportMenuView(request):

    context={
        "title": "Report",
        "open": "report",
        "obj_model":"report",
        **permissions(request)
    }
    return render(request, "rent/list-menu-reports.html", context )



class RoomTypeCreateView(LoginRequiredMixin, RoomTypeCreatePermissionMixin, CreateView):
    form_class = RegisterRoomTypeForm
    success_url = reverse_lazy('list-roomtypes')
    context_object_name = 'form'
    template_name = 'rent/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tab_name"] = "Register"
        context["title"] = "Room Type"
        context["card_header"] = "Register Room Type"
        context["open"] = "roomtype"

        return {**context, **permissions(self.request)}

    def form_valid(self, form):
        messages.success(self.request, 'Room Type Registered Successfully')
        return super().form_valid(form)


class RoomTypeUpdateView(LoginRequiredMixin, RoomTypeUpdatePermissionMixin, UpdateView):
    login_required = True
    model = RoomType
    form_class = RegisterRoomTypeForm
    context_object_name = "form"
    success_url = reverse_lazy("list-roomtypes")
    template_name = "rent/register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Room Type"
        context["card_header"] = "Update Room Type"
        context["open"] = "roomtype"
        
        return {**context, **permissions(self.request)}


    def form_valid(self, form):
        messages.success(self.request, 'Room Type Updated Successfully')
        form.instance.updated_by = self.request.user


        return super().form_valid(form)

class RoomTypeListView(LoginRequiredMixin, RoomTypeViewPermissionMixin, ListView):
    model = RoomType
    template_name = "rent/list-roomtype.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Room Type"
        context["open"] = "roomtype"
        context['obj_model'] = "roomtype"

        return {**context, **permissions(self.request)}

class RoomTypeDeleteView(LoginRequiredMixin, RoomTypeDeletePermissionMixin, DeleteView):
    model = RoomType
    template_name = "rent/delete_page.html"
    success_url = reverse_lazy('list-roomtypes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Room Type"
        context["open"] = "roomtype"
        context['obj_model'] = "roomtype" 
        
        
        return {**context, **permissions(self.request)}

    def delete(self, *args, **kwargs):
        if not self.get_object().room_set.all():
            super().delete(self, *args, **kwargs)
            messages.success(self.request, "Room Type Deleted successfully")

        else:
            messages.error(self.request, "Room Type Cant Be Deleted. Make sure there are no rooms under this Room Type ")
            
        return HttpResponseRedirect(self.success_url)
    
class PaymentDeleteView(LoginRequiredMixin, PaymentDeletePermissionMixin, DeleteView):
    model = Payment
    template_name = "rent/delete_page.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Payment"
        context["open"] = "payment"
        context['obj_model'] = "payment" 
        
        
        return {**context, **permissions(self.request)}

def MonthlyReportListView(request):
    month = request.GET.get("month", timezone.now().month)
    year = request.GET.get("year", timezone.now().year)
    reports = Payment.objects.filter(paid_date__month= month, paid_date__year = year)
    total = reports.aggregate(Sum('amount')).get("amount__sum")

    context = {
        "object_list":reports,
        "total":total,
        "open":"report",
        "title" :"Monthly Report",
        'obj_model': 'report',
        **permissions(request),
    }

    return render(request, "rent/list-monthly-report.html", context)


class ReportListView(LoginRequiredMixin, ReportViewPermissionMixin, ListView):
    model = Report
    template_name = "rent/list-report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Report"
        context["open"] = "report"
        context['obj_model'] = "report"

        return {**context, **permissions(self.request)} 



class UserListView(LoginRequiredMixin, UserViewPermissionMixin, ListView):
    model = User
    template_name = "rent/list-user.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "User"
        context["open"] = "user"
        context['obj_model'] = "user"

        return {**context, **permissions(self.request)} 


class UserCreateView(LoginRequiredMixin,UserCreatePermissionMixin, CreateView):
    model = User
    template_name = "rent/register.html"
    form_class = UserRegistrationForm

    success_url = reverse_lazy("list-users")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "User"
        context["open"] = "user"
        context["card_header"] = "Register User"
        context['obj_model'] = "user"

        return {**context, **permissions(self.request)} 



class UserUpdateView(LoginRequiredMixin,UserUpdatePermissionMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = "rent/register.html"
    success_url = reverse_lazy("list-users")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "User"
        context["open"] = "user"
        context["card_header"] = "Update User"
        context['obj_model'] = "user"

        return {**context, **permissions(self.request)} 



class UserAdditionalInfoUpdateView(UpdateView):
    model = UserAdditionalInfo
    template_name = "rent/register.html"
    form_class = UserAdditionalInfoForm
    success_url = reverse_lazy('list-users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects"] = self.get_object(self).user
        return context

    def get_object(self, queryset=None):
        
        queryset = User.objects.all()
        
        pk = self.kwargs.get(self.pk_url_kwarg)

        if pk is not None:
            queryset = queryset.filter(pk=pk)

        if pk is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        obj = queryset.get().useradditionalinfo
        return obj
        

        
    
