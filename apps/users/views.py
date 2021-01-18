
import re

import view as view
from django.http.response import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from apps.users.models import User
import logging



logger = logging.getLogger('django')
class Registered(View):

    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        # 1.接收数据
        # 2.验证数据
        #     1.用户名长度是否符合5-20位
        #     2.密码长度8-20位，由字母和数字下划线组成
        #     3.确认密码必须和密码一致
        #     4.手机号必须符合规则
        # 3.验证没问题数据入库
        # 4.返回数据

        data = request.POST
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
        mobile = data.get('mobile')

        if not all([username,password,password2,mobile]):
            return HttpResponseBadRequest('参数有问题')

        if not re.match(r'[a-zA-Z0-9_]{5,20}',username):
            return HttpResponseBadRequest('用户名不符合规则')

        if not re.match(r'[a-zA-Z0-9_]{8,20}',password):
            return HttpResponseBadRequest('密码不符合规则')

        if password != password2:
            return HttpResponseBadRequest('两次输入的密码不一致')

        if not re.match(r'^1[3-9]\d{9}',mobile):
            return HttpResponseBadRequest('手机号不符合规则')


        try:
            user = User.objects.create_user(username=username,password=password,mobile=mobile)
        except Exception as e:
            logger.error(e)

        from django.contrib.auth import login


        #return HttpResponse('注册成功')
        return redirect(reverse('index:index'))


# 如何判断用户名是否重复：
# 1.前端获取到用户名信息发送到后端，后端接收数据
# 2.后端接收到数据后查询数据库，是否有相同的数据，通过count数量为0则没有重复，为1则重复。
# 3，请求方式：get 或post ,敏感数据一般用post,现在我们用get就可以。get还分两种，一：www.meidu_mall:8000/username/?username=qky
# 二：www.meidu_mall:8000/username/qky/


class usernameview(View):
    def get(self,request,username):   #第二种get直接通过参数就可以得到数据，如果是第一种则要data = request.get(username)
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code':400,'errormsg':'数据库错误'})

        return JsonResponse({'count':count})


class Loginview(View):
    def get(self,request):
        #return HttpResponse('登录打通')
        return render(request,'login.html')