from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

#from Crud.models import Account
#from Crud.forms import AccountForm

#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from Crud.forms import SignUpForm

import logging
# Create your views here.

#登録
def regist(request):
    account = get_user_model()
    #POSTの時（新規であれ編集であれ登録ボタンが押されたとき）
    if request.method == 'POST':
        #フォームを生成
        #form = UserCreationForm(request.POST, instance=account)
        form = SignUpForm(request.POST)
        if form.is_valid(): #バリデーションがOKなら保存
            account = form.save(commit=False)
            account.save()
            request.session['form_data'] = request.POST
            session_form_data = request.session.get('form_data')
            return redirect('selbo:home')
    else: #GETの時（フォームを生成）
        form = SignUpForm()

    session_form_data = request.session.get('form_data')
    if session_form_data == None:
        return render(request, 'accounts/regist.html', dict(form=form, session_form_data=session_form_data))
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
#def login(request):
#    accounts = Account.objects.all().order_by('id') #値を取得
#    return render(request, 'accounts/login.html', {'accounts':accounts}) #第3引数⇒Templateに値を渡す
def my_view(request):
    if request.user.is_authenticated:
        return HttpResponse(f'認証済みです: {request.user.username}')
    else:
        return HttpResponse('未認証です')

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
