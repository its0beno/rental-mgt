from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('' , views.dashboard_page , name = 'home'),
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
    path("update-user/<int:pk>", views.UserUpdateView.as_view(), name = "update-user"),
    path("update-info/<int:pk>", views.UserAdditionalInfoUpdateView.as_view(), name = "update-info"),
    
]