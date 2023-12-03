from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_posts, name='my_posts'),
    path('create/', views.create_post, name='create_post'),
]
