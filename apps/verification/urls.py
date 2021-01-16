from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from apps.verification.views import Imageview,Smscodeview

from apps.users import views
app_name = 'apps.verification'
urlpatterns = [

  url(r'^code/(?P<uuid>[\w-]+)/',Imageview.as_view(),name='image'),
  url(r'^smscode/(?P<mobile>1[3-9]\d{9})/',Smscodeview.as_view(),name='smscode')
]
