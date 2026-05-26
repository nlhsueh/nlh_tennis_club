from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template import loader
from .models import Court, Booking
from members.models import Member
from courts.forms import BookingForm
from datetime import date
from django.contrib.auth.decorators import login_required

def courts(request):
  courts = Court.objects.all()
  courts = Court.objects.all()
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
            return render(request, 'booking.html', context)
        elif request.method == "POST":
            print ('POST method to booking form')
            print (f"request.POST: {request.POST}")
            member = None
            try:
                member = Member.objects.get(user=request.user)
            except Member.DoesNotExist:
                print (f'{request.user} is not a member')
            booking_form = BookingForm(request.POST)
            if booking_form.is_valid():
                booking_form.save()
                print ('Booking successfully (saved)')
                result = '預約成功！'
                success = True
            else:
                print ('Booking fails (form is not valid)')
                errors = booking_form.errors.as_text()
                result = f'預約失敗：{errors}'
                success = False
            context = {
                'booking_form': booking_form,
                'result': result, 
                'success': success,
                'member': member,
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
    member = getMember(request)
    if member:
        print ('member.firstname', member.firstname)
    context = {'member': member,
               'bookings': bookings}
    return render(request, 'my_bookings.html', context)

def getMember(request):
    print (request.user)
    try:
        member = Member.objects.get(user=request.user)
        print (member)
        return member
    except Member.DoesNotExist:
        print (f"The user {request.user} is not a member")
        return None
