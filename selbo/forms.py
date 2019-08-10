from django.forms import ModelForm
from selbo.models import Book

class BookForm(UserCreationForm):
    class Meta:
        model = Book
        fields = ('book_id', 'book_title', 'author_name', 'book_attribute')
