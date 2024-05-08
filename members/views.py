from django.http import HttpResponse
from members.models import Member
from django.template import loader
from django.shortcuts import render
from .forms import InputForm

# def members(request):
#     print ('request: ', request)
#     return HttpResponse("Hello world!")

def members(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('all_members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))


def details(request, id):
  mymember = Member.objects.get(id = id)
  template = loader.get_template('details.html')
  context = {
    'mymember': mymember,
  }
  return HttpResponse(template.render(context, request))

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def input(request):
  template = loader.get_template('input.html')
  context = {
    'form': InputForm()
  }
  return HttpResponse(template.render(context, request))

def input02(request):
  print (request.method)
  template = loader.get_template('input.html')
  context = {
    'form': InputForm()
  }
  return HttpResponse(template.render(context, request))