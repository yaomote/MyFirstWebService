from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView, LogoutView

from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

app_name = 'Crud'
urlpatterns = [
    url(r'^$', views.regist, name='regist'),
    url(r'^accounts/$', views.index, name='index'),
    url(r'^accounts/(?P<pk>\d+)/$', views.accounts_detail, name='accounts_detail'),
    path('accounts/login/', views.Login.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', views.Logout.as_view(template_name='registration/logout.html'), name='logout'),
    url(r'^accounts/add/$', views.edit, name='add'),
    url(r'^accounts/edit/(?P<id>\d+)$', views.edit, name='edit'),
    url(r'^accounts/delete/(?P<id>\d+)/$', views.delete, name='delete'),
    url(r'^accounts/detail/(?P<id>\d+)/$', views.detail, name='detail'),
]
