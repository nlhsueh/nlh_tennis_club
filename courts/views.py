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

  court_type = request.GET.get('court-type')
  city = request.GET.get('city')
  
  if court_type:
      courts = courts.filter(courttype=court_type)
  if city:
      courts = courts.filter(city=city)
      
  if request.headers.get('HX-Request'):
      return render(request, 'fragments/court_list.html', {'courts': courts})

  template = loader.get_template('all_courts.html')
  context = {
    'courts': courts,
  }
  return HttpResponse(template.render(context, request))

def booking_form(request, court_id):
    if not request.user.is_authenticated:
        return HttpResponse(f'''
        <div class="text-center" style="padding: 20px 0;">
          <p class="text-muted" style="font-size: 14px; margin-bottom: 14px;">請先登入後再進行預訂。</p>
          <a href="/login/?next=/courts/" class="btn btn-primary" style="padding: 8px 24px; font-size: 13px; border-radius: 99px;">前往登入</a>
        </div>
        ''')
    court = Court.objects.get(id=court_id)
    existing_bookings = Booking.objects.filter(court=court)
    today_date = date.today().strftime('%Y-%m-%d')
    
    return render(request, 'fragments/booking_form.html', {
        'court': court,
        'existing_bookings': existing_bookings,
        'today_date': today_date
    })

def check_availability(request):
    court_id = request.POST.get('court_id')
    booking_date = request.POST.get('booking_date')
    
    existing = Booking.objects.filter(
        court_id=court_id,
        date=booking_date
    ).exists()
    
    if existing:
        return HttpResponse('<span class="text-danger">此日期已被預訂</span>')
    else:
        return HttpResponse('<span class="text-success">可預訂</span>')

@login_required
def create_booking(request):
    if request.method == "POST":
        court_id = request.POST.get('court_id')
        booking_date = request.POST.get('booking_date')
        reason = request.POST.get('reason', '')
        try:
            court = Court.objects.get(id=court_id)
            booking = Booking(court=court, user=request.user, date=booking_date, reason=reason)
            booking.save()
            return HttpResponse(f'''
            <div class="text-center" style="padding: 10px 0;">
              <span style="font-size: 40px; display: block; margin-bottom: 10px;">✅</span>
              <h5 style="color: var(--green-dark); font-weight: 700; margin-bottom: 8px;">預訂成功！</h5>
              <p class="text-muted" style="font-size: 13px; margin-bottom: 16px;">您已成功預訂 {court.courtname} ({booking_date})。</p>
              <button type="button" class="btn btn-primary" data-bs-dismiss="modal" onclick="window.location.reload()" style="padding: 6px 20px; font-size: 13px;">確定</button>
            </div>
            ''', status=201)
        except Exception as e:
            court = Court.objects.get(id=court_id)
            existing_bookings = Booking.objects.filter(court=court)
            today_date = date.today().strftime('%Y-%m-%d')
            return render(request, 'fragments/booking_form.html', {
                'court': court,
                'existing_bookings': existing_bookings,
                'today_date': today_date,
                'reason': reason,
                'error_message': '發生錯誤，此日期已被預訂，請選擇其他日期！'
            })

from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt
def cancel_booking(request, booking_id):
    if request.method == "DELETE":
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            booking.delete()
            return HttpResponse('') # Return empty response to remove the row
        except Booking.DoesNotExist:
            return HttpResponse('<div class="alert alert-danger">找不到該筆預訂</div>', status=404)
    return HttpResponse('Method not allowed', status=405)

def details(request, id):
  court = Court.objects.get(id=id)
  
  if request.headers.get('HX-Request'):
      return render(request, 'fragments/court_detail_modal.html', {'court': court})
      
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
            try:
                member = Member.objects.get(user=request.user)
            except:
                print (f'{request.user} is not a member')
                pass
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
    if isinstance(member, HttpResponse):
        return member
    print ('member.firstname', member.firstname)
    context = {'member': member,
               'bookings': bookings}
    return render(request, 'my_bookings.html', context)

def getMember(request):
    print(request.user)
    try:
        member = Member.objects.get(user=request.user)
        print(member)
        return member
    except Member.DoesNotExist:
        # Fallback: Attempt to auto-link member by matching username to firstname
        if request.user.is_authenticated:
            username = request.user.username.lower()
            member = Member.objects.filter(firstname__iexact=username, user__isnull=True).first()
            if member:
                member.user = request.user
                member.save()
                print(f"Auto-linked member {member} to user {request.user}")
                return member
        print(f"The user {request.user} is not a member")
        return render(request, 'booking_error.html', None)
    except Exception as e:
        print(f"Error retrieving member: {e}")
        return render(request, 'booking_error.html', None)
