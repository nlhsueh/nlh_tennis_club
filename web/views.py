from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.contrib import auth

from web.forms import LoginForm

def login(request):
    ''' 登入 '''
    template = loader.get_template('login.html')
    message = ''
    if request.method == "POST":
        # 輸入登入資料後
        post_form = LoginForm(request.POST)
        if post_form.is_valid():
            username = post_form.cleaned_data['username']
            password = post_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                message = f'{username} login successfully'
                main_html = loader.get_template('main.html')
                context = {'user': request.user}
                return HttpResponse(main_html.render(context, request))
            else:
                message = 'Login failed.'
            print (message)
    else:
        # 載入登入頁
        post_form = LoginForm()
    context = {
        'user':request.user,
        'post_form': post_form,
        'message': message,
    }
    return HttpResponse(template.render(context, request))


def logout(request):
    ''' 登出 '''
    auth.logout(request)
    main_html = loader.get_template('main.html')
    context = {'user': request.user}
    return HttpResponse(main_html.render(context, request))