from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib import auth
from django.shortcuts import render

from web.forms import LoginForm

def login(request):
    ''' 登入 '''
    login_page = loader.get_template('login.html')
    if request.method == 'GET':
        login_form = LoginForm()
        context = {
            'user': request.user,
            'login_form': login_form,
        }
        return render(request, 'login.html', context)
    elif request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                main_page = loader.get_template('main.html')
                context = {'user': request.user,
                           'message': 'login ok'}
                return render(request, 'main.html', context)
            else:
                err_login_msg = 'Login failed (user id/passworld not correct)'
        else:                    
            err_login_msg = 'Login error (login form is not valid)'

        # login fail
        context = {'login_form': login_form, 
                   'err_login_msg': err_login_msg}
        return render(request, 'login.html', context)
    
    else:
        print ('Error on request (not GET/POST)')


def logout(request):
    ''' 登出 '''
    auth.logout(request)
    main_html = loader.get_template('main.html')
    context = {'user': request.user}
    return HttpResponse(main_html.render(context, request))