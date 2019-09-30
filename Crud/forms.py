from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm

class SignUpForm(UserCreationForm):
    username = forms.CharField(required=True, label="ユーザ名")
    email = forms.EmailField(required=True, label="メールアドレス")

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザ名'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレス'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'パスワード'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'パスワード（確認）'


class LoginForm(AuthenticationForm):
    #ログオンフォームの定義
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fields in self.fields.values():
            fields.widget.attrs['class'] = 'form-control'
            fields.widget.attrs['placeholder']= fields.label


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            'profile_img',
            'username',
            'email',
        )

    def __init__(self, username = None, email=None, profile_img=None, password=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        #更新前の情報をフォームにセット
        if profile_img:
            self.fields['profile_img'].widget.attrs['profile_img'] = profile_img
        if username:
            self.fields['username'].widget.attrs['value'] = username
        if email:
            self.fields['email'].widget.attrs['value'] = email

    def update(self, user):
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.save()


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
