from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from apps.users import views
app_name = 'apps.users'
urlpatterns = [

    url(r'^register/$',views.Registered.as_view(),name='register')
]
