from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template import loader
from .models import Court, Booking
from courts.forms import BookingForm

# Create your views here.
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


def booking(request, place_id):
    if request.user.is_authenticated:
        template = loader.get_template('booking.html')
        message = ''
        if request.method == 'GET':
            post_form = BookingForm(initial={
                'place': place_id,
                'user': request.user})
        elif request.method == "POST":
            post_form = BookingForm(request.POST)
            if post_form.is_valid():
                post_form.save()
                message = 'Booking success.'
        else:
            return HttpResponseBadRequest()
        context = {
            'post_form': post_form,
            'message': message,
        }
        return HttpResponse(template.render(context, request))
    return redirect('login')


def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    print (request.user)
    for b in bookings:
        print (b)
    template = loader.get_template('my_bookings.html')
    context = {
        'bookings': bookings,
    }
    return HttpResponse(template.render(context, request))