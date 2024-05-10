from django.http import HttpResponse
from members.models import Member
from django.template import loader
from django.shortcuts import render
from .forms import CheckMemberForm, NewMemberForm

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

def check_member(request):
  if request.method == 'GET':

    if request.GET:
      # get request from get submission
      print ('提交 last form 後的 GET')
      print (request.GET)
      who_you_input = request.GET['last_name']
      print ('who_you_input', who_you_input)
      members = Member.objects.filter(lastname = who_you_input)
      checked_members_page = loader.get_template('checked_members.html')
      context = {
        "lastname": who_you_input,
        "checked_members": members
      }
      return HttpResponse(checked_members_page.render(context, request))      
    else:
      # original GET request
      print ('第一次載入 form')
      checking_member_page = loader.get_template('check_member.html')
      context = {
        'form': CheckMemberForm()
      }
      return HttpResponse(checking_member_page.render(context, request))
  
def new_member(request):
  if request.method == 'GET':
    template = loader.get_template('new_member.html')
    context = {
      'form': NewMemberForm()
    }
    return HttpResponse(template.render(context, request))
  elif request.method == 'POST':
    new_member_form = NewMemberForm(request.POST)
    print ('new member form is created')
    print (new_member_form)
    if new_member_form.is_valid():
        print ('valid and to save()')
        new_member_form.save()
        result = 'save ok'
    else:
        result = new_member_form.errors.as_data()
    template = loader.get_template('new_member_result.html')
    return HttpResponse(template.render({'result':result}, request))  