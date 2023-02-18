from django.forms import ModelForm
from django import forms
from django.forms import ClearableFileInput
from .models import Product,ProductMultipleImages
from customadmin.models import Orders



# class signupform(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=True, help_text='Required')
#     last_name = forms.CharField(max_length=30, required=True, help_text='Required' )
#     email = forms.EmailField(max_length=50, required=True, help_text='Required')
#     # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered")
#     phone = forms.IntegerField(min_value=1000000000, max_value=9999999999, required=True)

    
    # class Meta:
    #     model = User
    #     fields = ['username','first_name','last_name','email','phone',]
    

# class UpdateForm(ModelForm):
#     pass

# class user_UpdateForm(ModelForm):
#     class Meta:
#         model = UserInfo
#         fields = "__all__"
#         required_fields = ['username', 'email', 'password']
#         widgets = {
#             'email': forms.TextInput(attrs={'class': ' form-control mb-3 '}),
#             'username': forms.TextInput(attrs={'class': 'form-control mb-3'}),
#             'password': forms.TextInput(attrs={'class': 'form-control mb-3'})
#         }
#         labels = {
#             'email': 'email',
#             'username': 'Username',
#             'password': 'Password'
#         }       

class ProductForm(forms.ModelForm):
    main_image = forms.FileField()
    class Meta:
        model=Product
        fields = ['category', 'main_image']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductMultipleImages
        fields = ['image']
        widgets = {
            'image': ClearableFileInput(attrs={'multiple': True}),
        }
        
    
class OrderForm(forms.ModelForm):
    main_image = forms.FileField()
    class Meta:
        model=Orders
        fields = ['order_status', 'payment_status', 'payment_method']
        
