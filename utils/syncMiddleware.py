from django.utils.deprecation import MiddlewareMixin

from cart.models import ShoppingCart


class SessionSyncMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        # 没有登录就不用做数据同步
        # 登录情况才做数据从session同步到数据库，且重新更新session数据
        user_id = request.session.get('user_id')
        if user_id:
            # 登录情况
            session_goods = request.session.get('goods')
            if session_goods:
                # 1.判断session中商品是否存在于数据库中，如果存在则更新
                # 2.如果不存在则创建
                shop_carts = ShoppingCart.objects.filter(user_id=user_id)

                # 更新购物车中的商品数量，记录更新商品的id值
                data = []
                for goods in shop_carts:
                    for se_goods in session_goods:
                        if se_goods[0] == goods.goods_id:
                            goods.nums = se_goods[1]
                            goods.save()
                            data.append(se_goods[0])

                # 添加
                session_goods_ids = [i[0] for i in session_goods]
                add_goods_ids = list(set(session_goods_ids) - set(data))
                for add_goods_id in add_goods_ids:
                    for session_good in session_goods:
                        if add_goods_id == session_good[0]:
                            ShoppingCart.objects.create(user_id=user_id, goods_id=add_goods_id, nums=session_good[1])

            # 将数据库同步到session
            new_shop_carts = ShoppingCart.objects.filter(user_id=user_id)
            session_new_goods = [[i.goods_id, i.nums, i.is_select] for i in new_shop_carts]
            request.session['goods'] = session_new_goods

        return response
