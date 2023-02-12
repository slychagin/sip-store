from django.urls import path

from blog import views


urlpatterns = [
    path('', views.blog_page, name='blog_page'),
    # path('', views.BlogPageView.as_view(), name='blog'),
    # path(
    #     'category/<slug:category_slug>/',
    #     views.ProductsByCategoryListView.as_view(),
    #     name='products_by_category'
    # ),
    # path(
    #     'category/<slug:category_slug>/<slug:product_slug>/',
    #     views.ProductDetailView.as_view(),
    #     name='product_details'
    # ),
    # path('search/', views.SearchListView.as_view(), name='search')
]
