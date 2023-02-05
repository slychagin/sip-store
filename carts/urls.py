from django.urls import path

from carts import views


urlpatterns = [
    path('', views.cart_page, name='cart'),
    path('add_cart/', views.add_cart, name='add_cart'),
    path('plus/', views.plus_quantity, name='plus_quantity'),
    path('minus/', views.minus_quantity, name='minus_quantity'),
    path('delete/', views.cart_delete, name='cart_delete'),
]
