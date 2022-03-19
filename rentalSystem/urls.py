from django.contrib import admin
from django.urls import path , include
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rent.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='rent/login.html'), name = 'login'),
    path('logout/',views.logout,name='logout'),
    path('forgot/',views.forgot,name='forgot'),
    path('forgot/security-question/',views.forgot_password,name='forgot-password'),
    path('change-password/', views.PasswordChangeView.as_view(),name='change-password'),

]
