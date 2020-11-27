from django.urls import path
from .views import *

urlpatterns = [
    path('',home.as_view(),name='home'),    
    path('posts/create/',create_post.as_view(),name='newpost'),
    # path('posts/<int:pk>/',view_post.as_view(),name='view-post'),
    path('posts/<int:pk>/',viewpost,name='view-post'),
    path('posts/category/<str:category>/',view_category.as_view(),name='category-post'),
    path('posts/<str:username>/',view_post_by_author.as_view(),name='view-author-post'),
    path('posts/<int:pk>/update/',update_post.as_view(),name='update-post'),
    path('posts/<int:pk>/delete/',delete_post.as_view(),name='delete'),
    path('blog/about',about,name='about'),
    path('blog/search',search.as_view(),name='search'),

]