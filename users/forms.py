from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# create form for panel admin & user
class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = "__all__"

    def clean_password2(self):
        data = self.cleaned_data
        if data['password2'] and data['password1'] and data['password'] != data['password1']:
            raise forms.ValidationError('pls check agne ...')
        return data['password2']

    def save(self, commit=True):
        user = super.save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = User
        fields = "__all__"

    def clean_password(self):
        return self.initial['password']

