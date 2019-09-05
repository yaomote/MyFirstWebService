#2019/07/21 更新

from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'selbo'
urlpatterns = [
    #url(r'^$', views.home, name='home'),
    path('', views.IndexView.as_view(), name='home'),
]
