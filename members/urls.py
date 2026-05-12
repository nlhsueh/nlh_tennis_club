from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('members/', views.members, name='members'),
    path('members/details/<int:id>', views.details, name='details'),
    path('members/member_detail/<int:id>', views.member_detail, name='member_detail'),
    path('members/edit/<int:id>', views.edit_member_form, name='edit_member_form'),
    path('members/update/<int:id>', views.update_member, name='update_member'),
]