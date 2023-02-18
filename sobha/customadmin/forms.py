from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,UsernameField,PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from .models import Customer
from django.contrib.auth import password_validation






class Loginform(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control'}))


class CustomerProfileForm(forms.ModelForm):
  class Meta:
    model = Customer
    fields = ['first_name','last_name','email','phone_number','address', 'city','district','pincode', 'state']
    widgets = {'first_name':forms.TextInput(attrs={'class':'form-control'}), 'last_name':forms.TextInput(attrs={'class':'form-control'}), 'email':forms.EmailInput (attrs={'class':'form-control'}), 'phone_number':forms.NumberInput(attrs={'class':'form-control'}), 'address':forms.TextInput(attrs={'class':'form-control'}), 'city':forms.TextInput(attrs={'class':'form-control'}), 'district':forms.TextInput(attrs={'class':'form-control'}), 'pincode':forms.NumberInput(attrs={'class':'form-control'}), 'state':forms.Select(attrs={'class':'form-control'}),}


class MyPasswordChangeForm(PasswordChangeForm):
 old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus':True,  'class':'form-control'}))
 new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
 new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}))


