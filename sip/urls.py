from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from sip import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
