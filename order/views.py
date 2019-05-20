from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from cart.models import ShoppingCart
from order.models import OrderInfo, OrderGoods
from user.models import UserAddress
from utils.functions import get_order_sn


def place_order(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        shop_carts = ShoppingCart.objects.filter(user_id=user_id, is_select=1)
        user_address = UserAddress.objects.filter(user_id=user_id)
        # 给购物车中的对象绑定一个新增的属性，其值为小计价格
        all_total = 0
        for carts in shop_carts:
            carts.price = carts.nums * carts.goods.shop_price
            all_total += carts.price
        # 结算商品个数，总价
        carts_count = len(shop_carts)

        return render(request, 'place_order.html', {'shop_carts': shop_carts, 'carts_count': carts_count,
                                                    'all_total': all_total, 'user_address': user_address})


def make_order(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        # 取购物车中勾选的商品
        shop_carts = ShoppingCart.objects.filter(user_id=user_id, is_select=1)
        # 计算下单的总价
        order_mount = 0
        for carts in shop_carts:
            order_mount += carts.nums * carts.goods.shop_price
        # 生成订单交易号
        order_sn = get_order_sn()
        # 1.创建订单
        address_id = int(request.POST.get('address_id'))
        user_address = UserAddress.objects.filter(pk=address_id).first()
        order = OrderInfo.objects.create(user_id=user_id, order_sn=order_sn, order_mount=order_mount,
                                         address=user_address.address, signer_name=user_address.signer_name,
                                         signer_mobile=user_address.signer_mobile)
        # 2.创建订单详情
        for carts in shop_carts:
            OrderGoods.objects.create(order=order, goods=carts.goods, goods_nums=carts.nums)
        # 3.删除购物车中的商品
        shop_carts.delete()
        request.session.pop('goods')

        return JsonResponse({'code': 200, 'msg': '请求成功'})
