from django.contrib import admin
from django.urls import path, include




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rent.urls')),
    path('accounts/', include('authentication.urls')),
]


handler404 = 'authentication.views.page_not_found_view'
handler500 = 'authentication.views.error_view'
handler403 = 'authentication.views.permission_denied_view'
handler400 = 'authentication.views.bad_request_view'