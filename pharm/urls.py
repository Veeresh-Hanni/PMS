from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from pharmacy.views import custom_error_view

handler400 = 'pharmacy.views.custom_error_view'
handler403 = 'pharmacy.views.custom_error_view'
handler404 = 'pharmacy.views.custom_error_view'
handler500 = 'pharmacy.views.custom_error_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pharmacy.urls')),
    path('', include('django.contrib.auth.urls')),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
