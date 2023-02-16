from django.urls import path

from orders import views


urlpatterns = [
    path('', views.OrderFormView.as_view(), name='order_form')
]
