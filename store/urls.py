from django.urls import path

from store import views

urlpatterns = [
    path('', views.StorePageView.as_view(), name='store'),
    path(
        'category/<slug:category_slug>/',
        views.ProductsByCategoryListView.as_view(),
        name='products_by_category'
    ),
    path(
        'category/<slug:category_slug>/<slug:product_slug>/',
        views.ProductDetailView.as_view(),
        name='product_details'
    ),
    path('search/', views.SearchListView.as_view(), name='search'),
    path('load-more/', views.load_more_reviews, name='load_more_reviews'),
]
