#2019/07/21 更新

from django.conf.urls import url
from selbo import views
from django.urls import path

app_name = 'selbo'
urlpatterns = [
    #url(r'', views.index, name='index'),
    path('', views.SignUpView.as_view(), name = 'signup'),
]
