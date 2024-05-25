from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('members/', views.members, name='members'),
    path('members/query', views.query_member, name='query'),
    path('members/details/<int:id>', views.details, name='details'),
]