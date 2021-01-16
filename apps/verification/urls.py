from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from apps.verification.views import Imageview

from apps.users import views
app_name = 'apps.verification'
urlpatterns = [

  url(r'^code/(?P<uuid>[\w-]+)/',Imageview.as_view(),name='image'),

]
