from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout as django_logout
from .forms import SignupForm, LoginForm
from .models import monitor
from django.views.decorators.csrf import csrf_exempt
from generator.models import class_cnt, problem
from django.contrib.auth.decorators import login_required

import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:  # 오류상황
        form = SignupForm()
    return render(request, 'accounts/signup.html', {
        'form': form,  # 로그인 요청하는 페이지로 다시 이동
    })

@csrf_exempt
def login(request):
    # if there is no class_cnt instance, make one instance
    cnt_class = class_cnt.objects.all().count()
    if cnt_class == 0:
        class_cnt().save()


    if request.method == "POST":
        form = LoginForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')

        if monitor.objects.filter(email=email).exists():
            cur_monitor = monitor.objects.get(email=email)

            if cur_monitor.password == password:
                problem_num = problem.objects.filter(ID=email).count()
                context = {'email':email, 'PN' : problem_num}
                request.session['user']=email

                return render(request, 'generator/Dashboard.html', context)
            else:
                return render(request, 'main/Alarm_Manage.html')

        return render(request, 'accounts/login_fail.html')

    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {"form": form})

@csrf_exempt
def logout(request):
    django_logout(request)
    return redirect("/")
