from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from sip import views

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('sip-secure/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='home'),
    path('quick-show/', views.get_single_product, name='get_single_product'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    path('contacts/', include('contacts.urls')),
    path('order/', include('orders.urls')),
    path('blog/', include('blog.urls')),
    path('wishlist/', include('wishlist.urls'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
