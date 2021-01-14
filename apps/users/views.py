import re

import view as view
from django.http.response import HttpResponseBadRequest,HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View




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
        from apps.users.models import User
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


        user = User.objects.create_user(username=username,password=password,password2=password2,mobile=mobile)

        return HttpResponse('注册成功')





