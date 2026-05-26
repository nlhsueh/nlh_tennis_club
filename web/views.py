from django.contrib.auth import authenticate
from django.contrib import auth
from django.shortcuts import render
from datetime import date

from web.forms import LoginForm
from members.models import Member

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
                # 檢查該 user 是否有 Member Profile，如果沒有則自動新建一個
                if not hasattr(user, 'member'):
                    Member.objects.create(
                        user=user,
                        firstname=user.username,
                        lastname="系統預建",
                        phone=None,
                        joined_date=date.today()
                    )
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