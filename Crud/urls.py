from django.conf.urls import url
from . import views

app_name = 'Crud'
urlpatterns = [
    url(r'^$', views.regist, name='regist'),
    url(r'^accounts/$', views.index, name='index'),
    url(r'^accounts/(?P<pk>\d+)/$', views.accounts_detail, name='accounts_detail'),
    url(r'^accounts/add/$', views.edit, name='add'),
    url(r'^accounts/edit/(?P<id>\d+)$', views.edit, name='edit'),
    url(r'^accounts/delete/(?P<id>\d+)/$', views.delete, name='delete'),
    url(r'^accounts/detail/(?P<id>\d+)/$', views.detail, name='detail'),
]
