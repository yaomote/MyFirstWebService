from django.forms import ModelForm
from selbo.models import Book
from django import forms

#class BookForm(UserCreationForm):
#    class Meta:
#        model = Book
#        fields = ('book_id', 'book_title', 'author_name', 'book_attribute')

class SearchForm(forms.Form):
    attribute = forms.CharField(
        initial = '',
        label = 'なりたい気分',
        required = True,
    )
    #image = forms.ImageField()
