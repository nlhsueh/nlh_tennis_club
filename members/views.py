from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Member

from django.contrib.staticfiles import finders

from django.db.models import Q

# Create your views here.
def members(request):
    mymembers = Member.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        mymembers = mymembers.filter(
            Q(firstname__icontains=search_query) |
            Q(lastname__icontains=search_query)
        )
    template = loader.get_template('all_members.html')
    context = {
      'mymembers': mymembers,
      'search_query': search_query,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    mymember = Member.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
      'mymember': mymember,
    }
    return HttpResponse(template.render(context, request))

def main(request):
    print ('main is called')
    print(request.session.items()) 
    
    # Print the paths of static files to show they are correctly found
    print("=== Checking Static Files ===")
    for static_file in ["css/club.css", "img/centre.jpeg", "img/garros.png"]:
        absolute_path = finders.find(static_file)
        print(f"Static file '{static_file}' found at: {absolute_path}")
    print("=============================")

    template = loader.get_template('main.html')
    return HttpResponse(template.render({}, request))

def testing(request):
    template = loader.get_template('template.html')
    context = {
      'fruits': ['Apple', 'Banana', 'Cherry'],   
    }
    return HttpResponse(template.render(context, request))