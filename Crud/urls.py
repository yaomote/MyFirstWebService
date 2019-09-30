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
    path('accounts/<int:pk>/', views.accounts_detail, name='accounts_detail'),
    path('accounts/login/', views.Login.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', views.Logout.as_view(template_name='registration/logout.html'), name='logout'),
    path('accounts/edit/<int:pk>/', views.UserUpdate.as_view(), name='edit'),
    path('accounts/edit/<int:pk>/password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('accounts/edit/<int:pk>/password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('accounts/edit/<int:pk>/delete/', views.UserDeleteView.as_view(), name='delete'),
]
