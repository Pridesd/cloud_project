from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('today/', views.today),
    path('forecast/', views.forecast),
    path('cloudsea/', views.cloudsea),

]
