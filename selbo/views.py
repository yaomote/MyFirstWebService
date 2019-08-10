from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

import urllib.request, urllib.error
from bs4 import BeautifulSoup
import time

from selbo.models import Book

import logging

# Create your views here.
def home(request):
    session_form_data = request.session.get('form_data')

    book = Book()

# Web Scraping
    for i in range(15):
        # アクセスするURL
        url = f"https://bookmeter.com/books/{i+1}"
        #url = "https://bookmeter.com/books/13963455"
        # URLにアクセスする htmlが帰ってくる → <html><head><title>例例例</title></head><body....
        html = urllib.request.urlopen(url=url)
        # htmlをBeautifulSoupで扱う
        soup = BeautifulSoup(html, "html.parser")
        # タイトル要素を取得する → <title>例例例例例例</title>
        title_tag = soup.find(class_='inner__title')
        #title_tag = soup.title
        # 要素の文字列を取得する → 例例例例例例
        title = title_tag.string
        logging.debug(title)
        # タイトル要素を出力
        #print title_tag
        # タイトルを文字列を出力
        #print title

        #データベースへ格納
        Book.objects.update_or_create(book_title=title)

        # スクレイピングの間隔を開ける
        time.sleep(5)

    if session_form_data == None:
        return redirect('Crud:regist')
    else:
        return render(request, 'selbo/home.html', dict(session_form_data=session_form_data))
