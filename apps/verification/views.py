from urllib import request

from django.shortcuts import render

from django.views import View
from django.http.response import HttpResponse, JsonResponse
from django_redis import get_redis_connection
from redis import StrictRedis

from libs.captcha.captcha import captcha
from libs.yuntongxun.sms import CCP


class Imageview(View):
    def get(self,request,uuid):

        #1.生成图片验证码和获取图片验证码内容
        text,image = captcha.generate_captcha()
        #2.连接reids
        redis_con = get_redis_connection('code')
        #3.把图片验证码保存到redis中 uuid:xxxx
        redis_con.setex(uuid ,1000,text)

        return HttpResponse(image,content_type='image/jpeg')



# 一.前端要做什么
# 1.前端要发送手机号，图形验证码，uuid给后端
# 二.后端大概业务逻辑
# 1.接收数据
# 2.验证数据
# 3.生成手机验证码
# 4.发送手机验证码
# 三.后端业务逻辑细化
# 1.接收数据
#     1.1接收手机号，客户输入的图形验证码，随机生成的uuid
# 2.验证数据
#     2.1验证手机号
#     2.2三个参数必须都有
#     2.3验证客户输入的图形码是否和redis保存的图形验证码一致
# 3.生成手机验证码
#     3.1生成手机验证码
#     3.2保存手机验证码  redis  key : value
# 4.发送手机验证码

# 请求方式：
# get
# 1. /smscode/mobile/uuid/imagecode/     URL
# 2./smscode/?mobile=xxxx&uuid=xxxx&imagecode=xxxx    查询字符串
# 3./smscode/(?P<mobile>1[3-9]\d{9})/?uuid=xxxx&imagecode=xxxx    混合式


class Smscodeview(View):#发送手机验证码
    def get(self,request,mobile):
        uuid = request.GET.get('uuid')  #接收前端uuid
        imagecode = request.GET.get('imagecode')#接收前端输入的图片验证码
        if not all(mobile):#     2.2三个参数必须都有
             return JsonResponse({'code':'0','smserror':'输入数据不全'})

        redis_con = get_redis_connection('code')#连接redis
        redis_code = redis_con.get(uuid)    #从reids提取数据
        redis_con.delete(uuid) #删除redis里的uuid
        # redis_code = str(redis_uuid,encoding='utf-8')  #python3后从redis得到的是二进制的，需要转化成str

        if redis_code is None:  #判断redis数据是否过期
            return JsonResponse({'code':'4001','codeerror':'验证码过期'})

        if redis_code.decode() != imagecode:  #比对输入的验证码和redis的是否一致
            return JsonResponse({'code':'4002','codeerror':'ERROR'})

        mark_mobile = redis_con.get('mark_%s'%mobile) #获取redis的标志
        if mark_mobile:#如果标志为真则报错
            return JsonResponse('发送过于频繁')

        from random import randint
        smscode = '%06d'%randint(0,999999)  #随机生成手机验证码

        pipe = redis_con.pipeline()#创建管道
        pipe.setex(mobile,60,smscode)#把手机验证码保存到redis中
        pipe.setex('mark_%s'%mobile,60,1) #设定标志
        pipe.execute()#执行管道
        #redis_con.delete(mobile)#删除redis里的mobile

        # CCP().send_template_sms(mobile,[smscode,5],1)  #发送验证码
        from celery_tasks.sms.tasks import send_sms_code
        send_sms_code.delay(mobile,smscode)#调用delay发送到队列

        return JsonResponse({'code':'200','smserror':'ok'})