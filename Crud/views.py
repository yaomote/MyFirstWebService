from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, login
from Crud.forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView

import logging
# Create your views here.

#登録
def regist(request):
    session_username = None
    account = get_user_model()
    #POSTの時（新規であれ編集であれ登録ボタンが押されたとき）
    if request.method == 'POST':
        #フォームを生成
        form = SignUpForm(request.POST)
        if form.is_valid(): #バリデーションがOKなら保存
            account = form.save(commit=False)
            account.save()
            request.session['username'] = request.POST['username']
            session_username = request.session['username']
            return redirect('selbo:home')
    else: #GETの時（フォームを生成）
        form = SignUpForm()

    if 'username' in request.POST and 'password' in request.POST:
        request.session['username'] = request.POST['username']
        request.session['password'] = request.POST['password']
    if 'username' in request.session and 'password' in request.session:
        session_username = request.session['username']
        logged_in = True
    if session_username == None:
        return render(request, 'accounts/regist.html', dict(form=form))
    else:
        return redirect('selbo:home')

#一覧
def index(request):
    accounts = get_user_model().objects.all().order_by('id') #値を取得
    return render(request, 'accounts/index.html', {'accounts':accounts}) #第3引数⇒Templateに値を渡す

#アカウントページ
def accounts_detail(request, pk):
    account = get_object_or_404(get_user_model(), pk=pk)
    return render(request, 'accounts/account_detail.html', {'account':account})

#ログイン
class Login(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    logged_in = False
    username = None

    def form_valid(self, form):
        login(self.request, form.get_user())
        if 'username' in self.request.POST and 'password' in self.request.POST:
            self.request.session['username'] = self.request.POST['username']
            self.request.session['password'] = self.request.POST['password']
        if 'username' in self.request.session and 'password' in self.request.session:
            session_username = self.request.session['username']
            logged_in = True
        return HttpResponseRedirect(self.get_success_url())

#ログアウト
class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'registration/logout.html'

#編集
def edit(request, id=None):
    if id: #idがあるとき（編集の時）
        #idで検索して、結果を戻すか、404エラー
        account = get_object_or_404(Account, pk=id)
    else: #idが無いとき（新規の時）
        #Accountを作成
        account = Account()
    #POSTの時（新規であれ編集であれ登録ボタンが押されたとき）
    if request.method == 'POST':
        #フォームを生成
        form = AccountForm(request.POST, instance=account)
        if form.is_valid(): #バリデーションがOKなら保存
            account = form.save(commit=False)
            account.save()
            return redirect('Crud:regist')
    else: #GETの時（フォームを生成）
        form = AccountForm(instance=account)
    #新規・編集画面を表示
    return render(request, 'accounts/edit.html', dict(form=form, id=id))

#削除
def delete(request, id=None):
    return HttpResponse("削除")
#詳細（おまけ）
def detail(request, id=None):
    return HttpResponse("詳細")
