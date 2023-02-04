from django.urls import path

from carts import views


urlpatterns = [
    path('', views.cart_page, name='cart'),
    path('add_cart/', views.add_cart, name='add_cart'),
    # path('add_quantity/<int:product_id>/', views.add_quantity, name='add_quantity'),
    # path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('delete/', views.cart_delete, name='cart_delete'),
]
