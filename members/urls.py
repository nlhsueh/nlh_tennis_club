from django.urls import path
from . import views

urlpatterns = [
    path('', views.members, name='members'),
    path('members/', views.members, name='members'),
]

print ('urlpatterns in called in members', urlpatterns)