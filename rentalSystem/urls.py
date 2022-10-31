from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rent.urls')),
    path('accounts/', include('authentication.urls')),
]+ static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT )


handler404 = 'authentication.views.page_not_found_view'
handler500 = 'authentication.views.error_view'
handler403 = 'authentication.views.permission_denied_view'
handler400 = 'authentication.views.bad_request_view'

admin.site.site_header = "Tenant Adminstration Panel"