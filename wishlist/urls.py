from django.urls import path

from wishlist import views


urlpatterns = [
    path('', views.wishlist_page, name='wish'),
    # path('add_cart/', views.add_cart, name='add_cart'),
    # path('plus/', views.plus_quantity, name='plus_quantity'),
    # path('minus/', views.minus_quantity, name='minus_quantity'),
    # path('delete/', views.cart_delete, name='cart_delete'),
    # path('mini_delete/', views.mini_cart_delete, name='mini_cart_delete'),
]