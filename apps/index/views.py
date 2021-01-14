from django.shortcuts import render

from django.views import View
from django.http.response import HttpResponse



class Index(View):
    def get(self,request):


        return render(request,'index.html')
