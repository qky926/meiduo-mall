from urllib import request

from django.shortcuts import render

from django.views import View
from django.http.response import HttpResponse
from django_redis import get_redis_connection


from libs.captcha.captcha import captcha

class Imageview(View):
    def get(self,request,uuid):

        #1.生成图片验证码和获取图片验证码内容
        text,image = captcha.generate_captcha()
        #2.连接reids
        redis_con = get_redis_connection('code')
        #3.把图片验证码保存到redis中 uuid:xxxx
        redis_con.setex(uuid,120,text)

        return HttpResponse(image,content_type='image/jpeg')
