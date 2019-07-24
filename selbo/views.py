from django.shortcuts import render
#from django.http import HttpResponse

# Create your views here.
#2019/07/21 追加
def index(request):
    return render(request, 'selbo/index.html')
