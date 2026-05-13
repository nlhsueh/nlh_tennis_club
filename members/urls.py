from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='/members/', permanent=False)),
    path('members/', views.members, name='members'),
    path('members/details/<int:id>', views.details, name='details'),
]