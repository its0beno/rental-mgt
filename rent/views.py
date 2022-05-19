from telnetlib import STATUS
from bot.message_sender import overdue_message_formatter
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render

from .forms import *
from .mixins import *


# Create your views here.

def permissions(request):
    context ={
        

        'building_permission': request.user.has_perm(perm="rent.view_building"),
        'building_add_permission': request.user.has_perm(perm="rent.add_building"),
        'building_change_permission': request.user.has_perm(perm="rent.change_building"),
        'building_delete_permission': request.user.has_perm(perm="rent.delete_building"),
        

        'renter_permission': request.user.has_perm(perm="rent.view_renter"),
        'renter_add_permission': request.user.has_perm(perm="rent.add_renter"),
        'renter_change_permission': request.user.has_perm(perm="rent.change_renter"),
        'renter_delete_permission': request.user.has_perm(perm="rent.delete_renter"),


        'roomtype_permission': request.user.has_perm(perm="rent.view_roomtype"),
        'roomtype_delete_permission': request.user.has_perm(perm="rent.delete_roomtype"),
        'roomtype_add_permission': request.user.has_perm(perm="rent.add_roomtype"),
        'roomtype_change_permission': request.user.has_perm(perm="rent.change_roomtype"),


        'room_permission': request.user.has_perm(perm="rent.view_room"),
        'room_add_permission': request.user.has_perm(perm="rent.add_room"),
        'room_change_permission': request.user.has_perm(perm="rent.change_room"),
        'room_delete_permission': request.user.has_perm(perm="rent.delete_room"),


        'user_permission': request.user.has_perm(perm="auth.view_user"),  
        'user_add_permission': request.user.has_perm(perm="auth.add_user"),
        'user_change_permission': request.user.has_perm(perm="auth.change_user"),
        'user_delete_permission': request.user.has_perm(perm="auth.delete_user"),


        'payment_permission': request.user.has_perm(perm="rent.view_payment"),
        'payment_delete_permission': request.user.has_perm(perm="rent.delete_payment"),
        'payment_change_permission': request.user.has_perm(perm="rent.change_payment"),
        'payment_add_permission': request.user.has_perm(perm="rent.add_payment"),  

        'report_permission': request.user.has_perm(perm="rent.view_report"),

    }

    return context


@login_required
def dashboard_page(request):
    rooms = Room.objects.filter(is_active=True)
    renters = Renter.objects.filter(is_rented=True)
    payments = Payment.objects.all()
    rooms_rented_this_month = renters.filter(is_rented=True).filter(updated_date__year = timezone.now().year, updated_date__month = timezone.now().month).count()
    amount_collected_this_month = payments.filter(paid_date__year = timezone.now().year, paid_date__month = timezone.now().month).aggregate(Sum('amount')).get("amount__sum")
    this_year_balance = payments.filter(updated_date__year = timezone.now().year).aggregate(Sum('amount')).get("amount__sum")
    # Over Due Payments
    free_rooms = Room.objects.filter(status = "vacant").count()
    used_rooms = Room.objects.filter(status = "occupied").count()
    # over_due_payments = Report.objects.filter(payable_month = 1).count()
    reports = Report.objects.all()
    over_due = []
    for report in reports :
        if report.outstanding_balance >  0 :
            over_due.append(report)  
    
    over_due_payment = len(over_due)
    
   


    context = {
        "rooms": rooms,
        "renters": renters,
        "payments": payments,
        "rooms_rented_this_month": rooms_rented_this_month,
        "amount_collected_this_month": amount_collected_this_month,
        "this_year_balance": this_year_balance,
        "over_due_payments": over_due_payment,
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
        print("done")
        messages.success(self.request, 'Room Registered Successfully')
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user


        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


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
        return Renter.objects.filter(is_rented=True)
    



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
    template_name = 'rent/register_payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tab_name"] = "Register"
        context["title"] = "Payment"
        context["card_header"] = "Register Payment"
        context["open"] = "payment"

        return {**context, **permissions(self.request)}


    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'Payment Registered Successfully')
        

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
    if request.method == "POST":
        object.is_rented = False
        object.save()

        room = object.room
        if room.status == "occupied":
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
        if object.status == "occupied":
            messages.error(request, message="Room Can't be Deleted, you need to delete the rented attached to it")
        else:
            object.is_active=False
            object.save()
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
    buildings = Building.objects.all()



    context={
        "object_list": buildings,
        "title": "Reports",
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

    def form_valid(self, form):
        for i in range(1000):
            print("wow")
        if self.get_object().room_set.all().count() == 0 :
            super().form_valid(self)
            messages.success(self.request, "Room Type Deleted successfully")

        else:
            messages.error(self.request, "Room Type Cant Be Deleted. Make sure there are no rooms under this Room Type ")
            
        return HttpResponseRedirect(self.success_url)
        
class PaymentDeleteView(LoginRequiredMixin, PaymentDeletePermissionMixin, DeleteView):
    model = Payment
    template_name = "rent/delete_page.html"
    success_url = reverse_lazy('list-payments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Payment"
        context["open"] = "payment"
        context['obj_model'] = "payment" 
        
        
        return {**context, **permissions(self.request)}


# @login_required
# @permission_required(perm="rent.view_report", raise_exception=True)
# def MonthlyReportListView(request):
#     month = request.GET.get("month", timezone.now().month)
#     year = request.GET.get("year", timezone.now().year)
#     reports = Payment.objects.filter(paid_date__month= month, paid_date__year = year)
#     total = reports.aggregate(Sum('amount')).get("amount__sum")

#     context = {
#         "object_list":reports,
#         "total":total,
#         "open":"report",
#         "title" :"Monthly Report",
#         'obj_model': 'report',
#         **permissions(request),
#     }

#     return render(request, "rent/list-monthly-report.html", context)


@login_required
@permission_required(perm="rent.view_report", raise_exception=True)
def BuildingMonthlyReportListView(request, pk):
    month = request.GET.get("month", timezone.now().month)
    year = request.GET.get("year", timezone.now().year)
    reports = Payment.objects.filter(
              paid_date__month= month, 
              paid_date__year = year, 
              renter__room__building__id=pk
    )
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
        context["title"] = " Rental Balance Report"
        context["open"] = "report"
        context['obj_model'] = "report"

        return {**context, **permissions(self.request)} 

    def get_queryset(self):
        querset = Report.objects.filter(renter__room__building__id=self.kwargs.get('pk'))
        for object in querset.filter(renter__is_rented = True ):
            object.save() # make this using crone jobs
        return querset
    


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



class UserAdditionalInfoUpdateView(LoginRequiredMixin, UserUpdatePermissionMixin, UpdateView):
    model = UserAdditionalInfo
    template_name = "rent/register.html"
    form_class = UserAdditionalInfoForm
    success_url = reverse_lazy('list-users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects"] = self.get_object(self).user
        return {**context, **permissions(self.request)}

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
        

        
@login_required
def ChangeSecurity(request):
    security = UserAdditionalInfo.objects.get(user=request.user)
    confirmed = request.session.get("confirmed", False)
    if not confirmed:
        messages.error(request, "You're not confirmed yet.")
        return redirect("confirm-identity")

    if request.method == "POST":
        security_question = request.POST.get("security_question")
        security_answer = request.POST.get("security_answer")
        
        security.security_question = security_question
        security.security_answer = security_answer

        security.save()

        del(request.session['confirmed'])

        return redirect("home")
    
    
    context={
        "security_answer" : security.security_answer,
        "security_question" : security.security_question,
    }
    return render(request, "authentication/change-security.html", context)


def CheckPassword(request):
    if request.method == "POST":
        password = request.POST.get("password")
        if not request.user.check_password(password):
            messages.error(request, "Wrong Password")
            return redirect("confirm-identity")
        else:
            request.session["confirmed"] = True
            return redirect("change-security")
    
    return render(request, "authentication/check-password.html")




class UserDetailView(LoginRequiredMixin, UserViewPermissionMixin, DetailView):
    model = User
    template_name = "rent/user-detail.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "User"
        context["open"] = "userdetail"
        context['obj_model'] = "user"

        return {**context, **permissions(self.request)} 


@login_required
def UserDetail(request):
    object = request.user
    context = {
        "user": object,
        "title": "User",
        "obj_model": "user",
        **permissions(request),
    }

    return render(request, "rent/user-detail.html", context)

@login_required
def EditUserData(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        user = request.user

        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        user.save()

        messages.success(request, "Saved")
        return redirect("user-info")

    user = request.user

    context = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }

    return render(request, "authentication/change-user-info.html", context)

@login_required
@permission_required(perm = "rent.view_payment", raise_exception=True)
def OverDuePaymentListView(request):
    if request.method == 'POST':
        if "selected_id" in request.POST:
            due = []
            if request.POST["selected_id"]:
                for selected in request.POST.getlist("selected_id"):
                    var = []
                    var.append(Report.objects.get(id = selected).renter.full_name())
                    var.append(Report.objects.get(id = selected).renter.chat_id)
                    var.append(float(Report.objects.get(id = selected).outstanding_balance))
                    due.append(var)

            for info in due:
                overdue_message_formatter(info)

            messages.success(request, "Sent messages successfully.")
        else:
            messages.error(request, "You have to select at least one.")
    reports = Report.objects.all()
    over_due = []
    for report in reports :
        if report.outstanding_balance >  0 :
            over_due.append(report)  



    context = {
            "object_list": over_due,
            "open":"overdue",
            "title" :"Over Due Payments",
            'obj_model': 'over due',
            **permissions(request),
        }
    return render(request, "rent/over-due-list.html", context)


class BuildingListView(LoginRequiredMixin, BuildingViewPermissionMixin, ListView):
    model = Building
    template_name = "rent/building-list.html"



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Building"
        context["open"] = "building"
        context['obj_model'] = "building"
        
        
        return {**context, **permissions(self.request)}



class BuildingCreateView(LoginRequiredMixin, BuildingCreatePermissionMixin, CreateView):
    form_class = RegisterBuildingForm
    success_url = reverse_lazy('list-buildings')
    context_object_name = 'form'
    template_name = 'rent/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tab_name"] = "Bulding"
        context["title"] = "Building"
        context["card_header"] = "Register Building"
        context["open"] = "building"

        return {**context, **permissions(self.request)}

    def form_valid(self, form):
        messages.success(self.request, 'Building Registered Successfully')
        return super().form_valid(form)


class BuildingUpdateView(LoginRequiredMixin, BuildingUpdatePermissionMixin, UpdateView):
    login_required = True
    model = Building
    form_class = RegisterBuildingForm
    context_object_name = "form"
    success_url = reverse_lazy("list-buildings")
    template_name = "rent/register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Building"
        context["card_header"] = "Building"
        context["open"] = "building"

        return {**context, **permissions(self.request)}


    def form_valid(self, form):
        messages.success(self.request, 'Building Updated Successfully')
        return super().form_valid(form)


class BuildingDeleteView(LoginRequiredMixin, BuildingDeletePermissionMixin, DeleteView):
    model = Building
    success_url = reverse_lazy('list-buildings')
    template_name = "rent/delete_page.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Building"
        context["open"] = "building"
        context['obj_model'] = "building" 
        
        
        return {**context, **permissions(self.request)}


    def form_valid(self, form):
        if self.get_object().room_set.all().count() == 0 :
            super().form_valid(self)
            messages.success(self.request, "Building Deleted successfully")

        else:
            messages.error(self.request, "Building Cant Be Deleted. Make sure there are no rooms under this Building ")
            
        return HttpResponseRedirect(self.success_url)
        


@login_required
@permission_required(perm = "rent.view_report")
def RoomPrice(request, pk):
    renter = Renter.objects.get(id = pk)

    room_price = renter.room.total_price

    return JsonResponse({"price":room_price})


@login_required
@permission_required(perm = "rent.view_roomtype")
def RoomReport(request, pk):
    Rooms = RoomType.objects.all()


    context = {
        "room_types":[],
        "open":"report",
        "title" :"Room Report",
        'obj_model': 'report',
        **permissions(request),
    }
    
    for vacant in Rooms :
        vacant_rooms = vacant.room_set.filter(status = 'vacant', building__id=pk).count()

        total_rooms = vacant.room_set.filter(building__id=pk).count()
        data  = {
            'roomtype' : vacant.room_type,
            'vacant_rooms': vacant_rooms,
            'total_rooms': total_rooms
        }
        context['room_types'].append(data)
    print(context)    
    

    return render(request, "rent/room-report.html", context)



# class PenalityListView(LoginRequiredMixin, PaymentViewPermissionMixin, ListView):
#     model = Penality
#     template_name = "rent/penality-list.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = " Rental Balance Report"
#         context["open"] = "penality"
#         context['obj_model'] = "report"

#         return {**context, **permissions(self.request)} 


# class PenalityDeleteView(LoginRequiredMixin, PaymentDeletePermissionMixin, DeleteView):
#     model = Penality
#     template_name = "rent/delete_page.html"
#     success_url = reverse_lazy('list-penality')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Penality"
#         context["open"] = "penality"
#         context['obj_model'] = "penality" 
        
        
#         return {**context, **permissions(self.request)}



# class PenalityUpdateView(LoginRequiredMixin, PaymentUpdatePermissionMixin, UpdateView):
#     login_required = True
#     model = Penality
#     form_class = RegisterPenalityForm
#     context_object_name = "form"
#     success_url = reverse_lazy("list-penality")
#     template_name = "rent/register.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Penality"
#         context["card_header"] = "Update Penality"
#         context["open"] = "penality"


#         return {**context, **permissions(self.request)}



# class PenalityCreateView(LoginRequiredMixin, PaymentCreatePermissionMixin, CreateView):
#     form_class = RegisterPenalityForm
#     success_url = reverse_lazy('list-penality')
#     context_object_name = 'form'
#     template_name = 'rent/register.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["tab_name"] = "Register"
#         context["title"] = "Penality"
#         context["card_header"] = "Register Penality"
#         context["open"] = "penality"

#         return {**context, **permissions(self.request)}