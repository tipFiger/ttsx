from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from user.models import User

class UserLoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 登录校验中间件
        # 过滤不需要做登录校验的地址
        path = request.path
        if path in ['/user/register/', '/user/login/']:
            return None

        # 做登录校验
        user_id = request.session.get('user_id')
        if not user_id:
            return HttpResponseRedirect(reverse('user:login'))
        user = User.objects.get(pk=user_id)
        request.user = user





