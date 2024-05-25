from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Member
from .forms import QueryMemberForm

# Create your views here.
def members(request):
    mymembers = Member.objects.all().values()
    template = loader.get_template('all_members.html')
    context = {
      'mymembers': mymembers,
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
    template = loader.get_template('main.html')
    return HttpResponse(template.render({}, request))

def query_member(request):
    if request.method == 'GET':

        if request.GET:
            gender = request.GET['gender']
            members = Member.objects.filter(gender=gender)
            template = loader.get_template('queried_member.html')
            context = {
                "gender": gender,
                "queried_members": members
            }
            return HttpResponse(template.render(context, request))
        else:
            checking_member_page = loader.get_template('query_member.html')
            context = {
                'form': QueryMemberForm()
            }
            return HttpResponse(checking_member_page.render(context, request))        
    