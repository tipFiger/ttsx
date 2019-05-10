from datetime import datetime, timedelta

from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from user.form import RegisterForm, LoginForm
from user.models import User, UserToken
from utils.functions import get_token, is_login


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = make_password(form.cleaned_data.get('password'))
            User.objects.create(username=username, password=password)
            return HttpResponseRedirect(reverse('user:login'))
        errors = form.errors
        return render(request, 'register.html', {'errors': errors})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.get(username=username)
            # 校验密码是否一致
            if not check_password(password, user.password):
                pwd_error = '密码错误'
                return render(request, 'login.html', {'pwd_error': pwd_error})
            # 用户名和密码验证成功了，需要使用cookie+token进行登录身份标识
            res = HttpResponseRedirect(reverse('user:index'))
            token = get_token()
            res.set_cookie('token', token, max_age=86400)
            # res.delete_cookie('token')
            # 后端保存token参数值，用于用户下次访问时进行判断
            out_time = datetime.utcnow() + timedelta(days=1)
            my_token = UserToken.objects.filter(user_id=user.id).first()
            if my_token:
                my_token.token = token
                my_token.out_time = out_time
                my_token.save()
            else:
                UserToken.objects.create(token=token,
                                         user=user,
                                         out_time=out_time)
            return res

        errors = form.errors
        return render(request, 'login.html', {'errors': errors})


def logout(request):
    if request.method == 'GET':
        res = HttpResponseRedirect(reverse('user:index'))
        res.delete_cookie('token')
        return res



@is_login
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
