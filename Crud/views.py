from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from Crud.models import Account
from Crud.forms import AccountForm

#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

import logging
# Create your views here.

#登録
def regist(request):
    account = Account()
    #POSTの時（新規であれ編集であれ登録ボタンが押されたとき）
    if request.method == 'POST':
        #フォームを生成
        form = AccountForm(request.POST, instance=account)
        if form.is_valid(): #バリデーションがOKなら保存
            account = form.save(commit=False)
            account.save()
            request.session['form_data'] = request.POST
            session_form_data = request.session.get('form_data')
            #return render(request, 'accounts/home.html', dict(form=form, session_form_data=session_form_data))
            #return render(request, 'selbo/home.html', dict(session_form_data=session_form_data))
            return redirect('selbo:home')
    else: #GETの時（フォームを生成）
        form = AccountForm(instance=account)

    session_form_data = request.session.get('form_data')
    if session_form_data == None:
        return render(request, 'accounts/regist.html', dict(form=form, session_form_data=session_form_data))
    else:
        #return render(request, 'accounts/home.html', dict(form=form, session_form_data=session_form_data))
        #return render(request, 'selbo/home.html', dict(session_form_data=session_form_data))
        return redirect('selbo:home')

#一覧
def index(request):
    accounts = Account.objects.all().order_by('id') #値を取得
    return render(request, 'accounts/index.html', {'accounts':accounts}) #第3引数⇒Templateに値を渡す

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
