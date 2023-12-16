from django.urls import path
from . import views

urlpatterns = [
    path('', views.courts, name='courts'),
    # 127.0.0.1/courts              list all courts
    path('details/<int:id>', views.details, name='court_details'),
    # 127.0.0.1/courts/details/1    show the court#1
    path('bookings/', views.my_bookings, name='my_bookings'),
    # 127.0.0.1/courts/bookings     show the bookings of the logined user
    path('booking/<int:court_id>/', views.booking, name='booking'),
    # 127.0.0.1/courts/booking/1    booking the court#1
]