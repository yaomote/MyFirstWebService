from django.conf.urls import url
from Crud import views

app_name = 'Crud'
urlpatterns = [
    url(r'^members/$', views.index, name='index'),
    url(r'^members/add/$', views.edit, name='add'),
    url(r'^$', views.regist, name='regist'),
    url(r'^members/edit/(?P<id>\d+)$', views.edit, name='edit'),
    url(r'^members/delete/(?P<id>\d+)/$', views.delete, name='delete'),
    url(r'^members/detail/(?P<id>\d+)/$', views.detail, name='detail'),
]
