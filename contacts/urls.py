from django.urls import path

from contacts import views

urlpatterns = [
    path('', views.ContactsView.as_view(), name='contacts'),
    path('map-data/', views.map_data, name='map_data')
]
