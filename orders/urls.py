from django.urls import path

from orders import views

urlpatterns = [
    path('', views.OrderFormView.as_view(), name='order_form'),
    path('search-city/', views.post_city_search, name='post_city_search'),
    path('search-terminal/', views.post_terminal_search, name='post_terminal_search'),
    path('thanks/', views.ThanksPageView.as_view(), name='thanks')
]
