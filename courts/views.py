from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Court

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