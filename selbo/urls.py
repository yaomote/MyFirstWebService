#2019/07/21 更新

from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'selbo'
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('ajax/', views.ajax_add_post, name='ajax_add_post'),
]
