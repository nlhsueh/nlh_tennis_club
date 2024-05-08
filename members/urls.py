from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('members/', views.members, name='members'),
    path('members/details/<int:id>', views.details, name='details'),
    path('members/input', views.input, name='input'),
    path('members/input02', views.input02, name='input02'),
]