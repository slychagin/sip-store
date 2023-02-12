from django.urls import path

from orders import views


urlpatterns = [
    path('', views.place_order, name='place_order')
]
