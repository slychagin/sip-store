from django.urls import path

from blog import views

urlpatterns = [
    path('', views.BlogPageView.as_view(), name='blog_page'),
    path('category/<slug:slug>/', views.PostsByCategoryListView.as_view(), name='posts_by_category'),
    path('category/<slug:slug>/<int:pk>/', views.PostDetailView.as_view(), name='post_details'),
    path('load-more/', views.load_more_comments, name='load_more_comments'),
    path('search-post/', views.SearchListView.as_view(), name='search_post')
]
