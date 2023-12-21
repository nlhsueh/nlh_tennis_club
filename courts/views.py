from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template import loader
from .models import Court, Booking
from courts.forms import BookingForm
from datetime import date
from django.contrib.auth.decorators import login_required

def courts(request):
  courts = Court.objects.all().values()
  template = loader.get_template('all_courts.html')
  context = {
    'courts': courts,
  }
  return HttpResponse(template.render(context, request))

def details(request, id):
  court = Court.objects.get(id=id)
  template = loader.get_template('court_details.html')
  context = {
    'court': court,
  }
  return HttpResponse(template.render(context, request))

@login_required
def booking(request, court_id):
    print ('booking view is called')
    if request.user.is_authenticated:
        if request.method == 'GET':
            print ('GET method to booking form')
            initial = {
                'court': court_id,
                'user': request.user,
                'date': date.today(),
                'reason': '' }
            booking_form = BookingForm(initial)
            context = {'booking_form': booking_form}
            booking_page = loader.get_template('booking.html')
            # return HttpResponse(booking_page.render(context, request))
            return render(request, 'booking.html', context)
        elif request.method == "POST":
            print ('POST method to booking form')
            print (f"request.POST: {request.POST}")
            booking_form = BookingForm(request.POST)
            if booking_form.is_valid():
                booking_form.save()
                print ('Booking successfully (saved)')
                result = 'Booking ok'
            else:
                print ('Booking fails (form is not valid)')
                result = 'Booking fail'
            context = {
                'booking_form': booking_form,
                'result': result, 
            }    
            return render(request, 'booking_result.html', context)
        else:
            return HttpResponseBadRequest()

@login_required
def my_bookings(request):
    ''' to show my booking list '''
    bookings = Booking.objects.filter(user=request.user)
    print (f'All bookings by {request.user}:')
    for b in bookings:
        print (b)
    return render(request, 'my_bookings.html', {'bookings':bookings})