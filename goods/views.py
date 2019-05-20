from django.http import HttpResponseRedirect
from django.shortcuts import render

# 轮播图、商品分类和子类展示、
from django.urls import reverse

from goods.models import GoodsCategory, Goods


def index(request):
    if request.method == 'GET':
        data = {}
        # 循环商品分类
        for cate in GoodsCategory.CATEGORY_TYPE:
            # 获取当前分类下的前四个商品信息
            goods = Goods.objects.filter(category_id=cate[0])[0:4]
            # 组装成键值对，key为商品分类的名称，value为当前分类的商品信息
            data[cate[1]] = goods
        return render(request, 'index.html', {'goods_category': data})


def logout(request):
    if request.method == 'GET':
        request.session.flush()
        res = HttpResponseRedirect(reverse('goods:index'))
        return res


def detail(request,id):
    if request.method == 'GET':
        goods = Goods.objects.get(pk=id)
        return render(request, 'detail.html',{'goods':goods})


def goodlist(request):
    if request.method == 'GET':
        return render(request, 'list.html')
