#from django.shortcuts import render, redirect
#from django.http import HttpResponseRedirect
#
#import urllib.request, urllib.error
#from bs4 import BeautifulSoup
#import time
#
#from selbo.models import Book
#
#import logging
#
## Create your views here.
#def home(request):
#    session_username = None
#    if 'username' in request.POST and 'password' in request.POST:
#        request.session['username'] = request.POST['username']
#        request.session['password'] = request.POST['password']
#    if 'username' in request.session and 'password' in request.session:
#        session_username = request.session['username']
#        logged_in = True
#    book = Book()
#
#    if session_username == None:
#        return redirect('Crud:regist')
#    else:
#        return render(request, 'selbo/home.html', dict(session_username=session_username))


import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Book
from .forms import SearchForm
from django.db.models import Q
logger = logging.getLogger('development')
class IndexView(LoginRequiredMixin, generic.ListView):
    paginate_by = 5
    template_name = 'selbo/home.html'
    model = Book
    def post(self, request, *args, **kwargs):
        form_value = [
            self.request.POST.get('attribute', None),
        ]
        request.session['form_value'] = form_value
        # 検索時にページネーションに関連したエラーを防ぐ
        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()
        return self.get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # sessionに値がある場合、その値をセットする。（ページングしてもform値が変わらないように）
        attribute = ''
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            attribute = form_value[0]
        default_data = {'attribute': attribute, } # 本属性
        selbo_form = SearchForm(initial=default_data) # 検索フォーム
        context['selbo_form'] = selbo_form
        return context
    def get_queryset(self):
        # sessionに値がある場合、その値でクエリ発行する。
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            attribute = form_value[0]
            # 検索条件
            condition_attribute = Q()
            if len(attribute) != 0 and attribute[0]:
                condition_attribute = Q(book_attribute__icontains=attribute)
            return Book.objects.select_related().filter(condition_attribute)
        else:
            # 何も返さない
            return Book.objects.none()
