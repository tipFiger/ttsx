from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from cart.models import ShoppingCart


def cart(request):
    if request.method == 'GET':
        return render(request, 'cart.html')


def add_cart(request):
    if request.method == 'GET':
        session_goods = request.session.get('goods')
        goods_count = len(session_goods)
        return JsonResponse({'code': 200, 'msg': '请求成功', 'goods_count': goods_count})

    if request.method == 'POST':
        goods_id = int(request.POST.get('goods_id'))
        nums = int(request.POST.get('nums'))
        goods_list = [int(goods_id), int(nums), 1]
        session_goods = request.session.get('goods')

        if session_goods:
            # 添加或者修改
            flag = False
            for goods in session_goods:
                # goods为[goods_id, nums, is_select]
                if goods[0] == goods_id:
                    goods[1] += nums
                    flag = True
            # 添加
            if not flag:
                session_goods.append(goods_list)
            request.session['goods'] = session_goods
            # session中保存的商品的个数
            goods_count = len(session_goods)
        else:
            # 第一次添加商品到session中时，保存键值对
            # 键为goods，值为[[id, nums, is_select], [id, nums, is_select]]
            request.session['goods'] = [goods_list]
            goods_count = 1
        return JsonResponse({'code': 200, 'msg': '请求成功', 'goods_count': goods_count})


def count_cart(request):
    if request.method == 'GET':
        session_goods = request.session.get('goods')
        count = len(session_goods) if session_goods else 0
        return JsonResponse({'code': 200, 'msg': '请求成功', 'count': count})


def change_cart(request):
    if request.method == 'POST':
        # 获取前端Ajax传递的goods_id,is_select,nums
        goods_id = int(request.POST.get('goods_id'))
        is_select = request.POST.get('is_select')
        nums = request.POST.get('nums')
        # 获取session中商品的信息
        session_goods = request.session.get('goods')
        for goods in session_goods:
            if goods_id == goods[0]:
                # 修改session中的商品的数量和选择状态
                goods[1] = int(nums) if nums else goods[1]
                goods[2] = int(is_select) if is_select else goods[2]
        request.session['goods'] = session_goods
        return JsonResponse({'code': 200, 'msg': '请求成功'})


def del_cart(request, id):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        if user_id:
            # 登录情况，删除数据库中的数据
            ShoppingCart.objects.filter(user_id=user_id, goods_id=id).delete()
        # 不管登录与否，删除session中的数据
        session_goods = request.session.get('goods')
        for goods in session_goods:
            if goods[0] == int(id):
                session_goods.remove(goods)
        request.session['goods'] = session_goods
        return HttpResponseRedirect(reverse('cart:cart'))
