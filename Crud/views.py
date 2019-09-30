from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, login
from Crud.forms import SignUpForm, LoginForm, UserUpdateForm, MyPasswordChangeForm
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from selbo.models import Book
from django.views import generic
from django.urls import reverse, reverse_lazy

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
    context = {}
    account = get_object_or_404(get_user_model(), pk=pk)
    context['account'] = account
    context['book_regist_num'] = account.user_id.all().count()
    context['request_pk'] = int(pk)
    for book in account.user_id.all():
        context.setdefault('book_info', []).append([book.book_title, book.book_image.name])
    return render(request, 'accounts/account_detail.html', context)

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
class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        account = self.request.user
        return account.pk == self.kwargs['pk']

class UserUpdate(OnlyYouMixin, generic.UpdateView):
    model = get_user_model()
    template_name = 'accounts/edit.html'
    form_class = UserUpdateForm

    def form_valid(self, form):
        #ProfileEditFormのupdateメソッドにログインユーザを渡して更新
        form.update(user=self.request.user)
        return super().form_valid(form)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        #更新前のユーザ情報をkwargsとして渡す
        kwargs.update({
            'username': self.request.user.username,
            'email': self.request.user.email,
        })
        return kwargs

    def get_success_url(self):
        return reverse('Crud:accounts_detail', args=[self.request.user.id], )

class PasswordChange(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = MyPasswordChangeForm
    def get_success_url(self):
        return reverse('Crud:password_change_done', args=[self.request.user.id], )

class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'

#削除
class UserDeleteView(OnlyYouMixin, generic.DeleteView):
    model = get_user_model()
    template_name = 'accounts/delete.html'
    success_url = reverse_lazy('Crud:regist')
    slug_field = 'id'
    slug_url_kwarg = 'id'

    #def delete(self, request, *args, **kwargs):
    #    result = super().delete(request, *args, **kwargs)
    #    return result
