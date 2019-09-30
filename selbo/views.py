import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Book
from .forms import SearchForm
from django.db.models import Q

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
import json
from django.http import JsonResponse

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


def ajax_add_post(request):
    if 'username' in request.session and 'password' in request.session:
        session_username = request.session['username']
        print(f'*******************session_username = {session_username}')
        account = get_object_or_404(get_user_model(), username=session_username)

    book_id = request.POST.get("book_id", None)

    if get_user_model().objects.filter(user_id__book_id=book_id, username=account.username).first() is None:
        print('test1')
        print(get_user_model().objects.filter(user_id__book_id=book_id))
        account.user_id.add(Book.objects.get(book_id = book_id))
        user = {
            'flag': 'flag_on',
        }
        return JsonResponse(user)
    else :
        print('test2')
        print(get_user_model().objects.filter(user_id__book_id=book_id))
        account.user_id.remove(Book.objects.get(book_id = book_id))
        user = {
            'flag': 'flag_off',
        }
        return JsonResponse(user)
