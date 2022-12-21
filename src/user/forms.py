from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user:
            raise ValidationError('An account already exist for that email')
        return email


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))


class UserEditForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg'}))
    class Meta:
        model = User 
        fields = ['username', 'email']
    
    def clean_email(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exclude(username=username)
        if user:
            raise ValidationError('An account already exist for that email')
        return email
    


class ProfileEditForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control form-control-lg'}))
    class Meta:
        model = User 
        fields = ['image'] 

