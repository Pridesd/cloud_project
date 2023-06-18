from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:pk>/', views.post_detail, name='detail'),
    path('new_post/', views.new_post, name='new_post'),
    path('create_post/', views.create_post, name='create_post'),
    path('edit_post/<int:pk>', views.edit_post, name='edit_post'),
    path('update_post/<int:pk>', views.update_post, name='update_post'),
    path('delete_post/<int:pk>', views.delete_post, name='delete_post'),
    path('participate/<int:pk>', views.participate, name='participate')
]