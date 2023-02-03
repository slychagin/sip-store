from django.urls import path

from carts import views


urlpatterns = [
    path('', views.CartListView.as_view(), name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('add_quantity/<int:product_id>/', views.add_quantity, name='add_quantity'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
]
