from django.http import HttpResponse
from members.models import Member
from django.template import loader

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