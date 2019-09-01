from django.contrib import admin
#from Crud.models import Account
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import User

# Register your models here.
#admin.site.register(Account)

class MyUserChangeForm(UserChangeForm):
    class Meta:
        #model = User
        model = get_user_model()
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    class Meta:
        #model = User
        model = get_user_model()
        fields = ('email',)

        def clean_username(self):
            username = self.cleaned_data["username"]
            try:
                get_user_model().objects.get(username=username)
            except get_user_model().DoesNotExitst:
                return username
            raise forms.ValidationError(self.error_messages['duplicate_username'])


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(User, MyUserAdmin)
