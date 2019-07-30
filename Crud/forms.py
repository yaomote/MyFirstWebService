from django.forms import ModelForm
from Crud.models import Account


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'user_name', 'user_id', 'password')
