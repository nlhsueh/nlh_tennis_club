from django.http import HttpResponse

def members(request):
    print ('request: ', request)
    return HttpResponse("Hello world!")