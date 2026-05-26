from django.contrib.auth import authenticate
from django.contrib import auth
from django.shortcuts import render

from web.forms import LoginForm

def login(request):
    ''' 登入 '''
    message = None
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data['username'],
                password=login_form.cleaned_data['password'],
            )
            if user is not None:
                auth.login(request, user)
                return render(request, 'main.html', {
                    'user': request.user,
                    'message': 'login ok',
                })
            message = 'Login failed (auth fail)'
        else:
            message = 'Login error (login form is not valid)'
    else:
        login_form = LoginForm()

    print(message)
    return render(request, 'login.html', {
        'user': request.user,
        'login_form': login_form,
        'message': message,
    })


def logout(request):
    ''' 登出 '''
    auth.logout(request)
    # main_html = loader.get_template('main.html')
    context = {'user': request.user}

    return render(request, 'main.html', {
                    'user': request.user,
                })

    # return HttpResponse(main_html.render(context, request))