from django import forms
from django.forms import ModelForm
from .models import Account

class RegisterForm(ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Account
        fields = ['firstname','lastname','username','email',]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if confirm_password != password:
            self.add_error('confirm_password', "Password does not match")

         
        