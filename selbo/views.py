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

    if session_form_data == None:
        return redirect('Crud:regist')
    else:
        return render(request, 'selbo/home.html', dict(session_form_data=session_form_data))
