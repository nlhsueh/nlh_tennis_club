from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Member

# Create your views here.
def members(request):
    from django.db.models import Q
    mymembers = Member.objects.all()

    search_query = request.GET.get('search', '')
    if search_query:
        mymembers = mymembers.filter(
            Q(firstname__icontains=search_query) | 
            Q(lastname__icontains=search_query)
        )

    if request.headers.get('HX-Request'):
        return render(request, 'fragments/member_list.html', {'mymembers': mymembers})

    template = loader.get_template('all_members.html')
    context = {
      'mymembers': mymembers,
    }
    return HttpResponse(template.render(context, request))

def member_detail(request, id):
    mymember = Member.objects.get(id=id)
    return render(request, 'fragments/member_detail_modal.html', {'mymember': mymember})

def edit_member_form(request, id):
    member = Member.objects.get(id=id)
    return render(request, 'fragments/member_edit_form.html', {'member': member})

def update_member(request, id):
    member = Member.objects.get(id=id)
    if request.method == 'POST':
        member.firstname = request.POST.get('firstname')
        member.lastname = request.POST.get('lastname')
        member.phone = request.POST.get('phone')
        member.age = request.POST.get('age')
        member.save()
        return render(request, 'fragments/member_item.html', {'x': member})

def details(request, id):
    mymember = Member.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
      'mymember': mymember,
    }
    return HttpResponse(template.render(context, request))

def main(request):
    print ('main is called')
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def testing(request):
    template = loader.get_template('template.html')
    context = {
      'fruits': ['Apple', 'Banana', 'Cherry'],   
    }
    return HttpResponse(template.render(context, request))