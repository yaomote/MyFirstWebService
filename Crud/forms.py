from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from Crud.models import Account

class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'user_name', 'user_id', 'password')
        
#class LoginForm(AuthenticationForm):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        #htmlの表示を変更可能にします
#        self.fields['user_name'].widget.attrs['class'] = 'form-control'
#        self.fields['password'].widget.attrs['class'] = 'form-control'
