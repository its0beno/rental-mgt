from django.urls import path, reverse_lazy 
from . import views
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [
    path('' , views.dashboard_page , name = 'home'),
    path('user/', views.UserDetail, name="user-info"),
    path('user/edit/', views.EditUserData, name="edit-info"),
    path('user/confirm-identity', views.CheckPassword, name="confirm-identity"),
    path('user/change-security/', views.ChangeSecurity, name="change-security"),
    path('user/change-password/', PasswordChangeView.as_view(template_name="authentication/change-password.html", success_url = reverse_lazy("user-info")), name="user-change-password"),
    path("register-room/", views.RoomCreateView.as_view() , name="register-rooms"),
    path("list-rooms/", views.RoomListView.as_view(), name="list-rooms"),
    path("list-rooms/filter=<str:filter>/", views.RoomListView.as_view(), name="list-rooms"),
    path("detail-room/<int:pk>/", views.RoomDetailView.as_view(), name="detail-room"),
    path("edit-room/<int:pk>/", views.RoomUpdateView.as_view(), name="update-room"),
    path("delete-room/<int:pk>/", views.RoomDeleteView, name="delete-room"),
    path("register-renter/", views.RenterCreateView.as_view(), name= "register-renters"),
    path("list-renter/", views.RenterListView.as_view(), name= "list-renters"),
    path("detail-renter/<int:pk>/", views.RenterDetailView.as_view(), name= "detail-renter"),
    path("edit-renter/<int:pk>/", views.RenterUpdateView.as_view(), name= "update-renter"),
    path("delete-renter/<int:pk>/", views.RenterDeleteView, name="delete-renter"),
    path("register-payment/", views.PaymentCreateView.as_view(), name= "register-payments"),
    path("list-payment/", views.PaymentListView.as_view(), name= "list-payments"),
    path("detial-payment/<int:pk>/", views.PaymentDetailView.as_view(), name= "detail-payment"),
    path("edit-payment/<int:pk>/", views.PaymentUpdateView.as_view(), name= "update-payment"),
    path("list-menu-report/", views.ReportMenuView, name= "list-menu-reports"),
    path("list-roomtype/", views.RoomTypeListView.as_view(), name= "list-roomtypes"),
    path("update-roomtype/<int:pk>/", views.RoomTypeUpdateView.as_view(), name= "update-roomtype"),
    path("register-roomtype/", views.RoomTypeCreateView.as_view(), name= "register-roomtype"),
    path("delete-roomtype/<int:pk>/", views.RoomTypeDeleteView.as_view(), name= "delete-roomtype"),
    path("list-report-monthly/", views.MonthlyReportListView, name= "list-monthly-reports"),
    path("list-report/", views.ReportListView.as_view(), name= "list-reports"),
    path("list-users/", views.UserListView.as_view(), name = "list-users"),
    path("register-user/", views.UserCreateView.as_view(), name = "register-user"),
    path("update-user/<int:pk>/", views.UserUpdateView.as_view(), name = "update-user"),
    path("update-info/<int:pk>/", views.UserAdditionalInfoUpdateView.as_view(), name = "update-info"),
    path("user-detail/<int:pk>/", views.UserDetailView.as_view(), name = "user-detail"),
    path("payment-delete/<int:pk>/", views.PaymentDeleteView.as_view(), name = "payment-delete"),
    path("over-due/", views.OverDuePaymentListView, name = "over-due"),

    
]