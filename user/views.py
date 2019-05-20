from datetime import datetime, timedelta

from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from order.models import OrderInfo
from user.form import RegisterForm, LoginForm, UserAddressForm
from user.models import User, UserToken, UserAddress
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

            res = HttpResponseRedirect(reverse('goods:index'))
            # session中纯属user_id
            request.session['user_id'] = user.id
            request.session.set_expiry(86400)
            return res

        errors = form.errors
        return render(request, 'login.html', {'errors': errors})


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')


def user_center_info(request):
    if request.method == 'GET':
        return render(request, 'user_center_info.html')


def user_center_order(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        page_num = request.GET.get('page', 1)
        order_info = OrderInfo.objects.filter(user_id=user_id)
        paginator = Paginator(order_info, 5)
        page = paginator.page(page_num)
        return render(request, 'user_center_order.html', {'page': page})


def user_center_site(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        user_address = UserAddress.objects.filter(user_id=user_id)

        return render(request, 'user_center_site.html', {'user_address': user_address})

    if request.method == 'POST':
        # 使用表单做校验
        form = UserAddressForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('user_id')
            address = form.cleaned_data['address']
            signer_name = form.cleaned_data['signer_name']
            postcode = form.cleaned_data['postcode']
            mobile = form.cleaned_data['mobile']
            UserAddress.objects.create(user_id=user_id, address=address, signer_name=signer_name,
                                       signer_postcode=postcode, signer_mobile=mobile)

            return HttpResponseRedirect(reverse('user:user_center_site'))
        else:
            errors = form.errors

            return render(request, 'user_center_site.html', {'errors': errors})
