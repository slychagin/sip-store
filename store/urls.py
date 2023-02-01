from django.urls import path

from store import views


urlpatterns = [
    path('', views.StorePageView.as_view(), name='store'),
    path('<slug:category_slug>/', views.ProductsByCategoryListView.as_view(), name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.ProductDetailView.as_view(), name='product_details')
]
