from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from sip import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='home'),
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
