from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from apps.index import views
app_name = 'apps.index'
urlpatterns = [

    url(r'^$',views.Index.as_view(),name='index')
]