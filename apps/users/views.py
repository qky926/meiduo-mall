import view as view
from django.shortcuts import render

# Create your views here.
from django.views import View


class Registered(View):

    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        pass