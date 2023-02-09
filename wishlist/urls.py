from django.urls import path

from wishlist import views


urlpatterns = [
    path('', views.wishlist_page, name='wish'),
    path('add-wishlist/', views.add_wishlist, name='add_wishlist'),
    path('wishlist-delete/', views.wishlist_delete, name='wishlist_delete'),
]
