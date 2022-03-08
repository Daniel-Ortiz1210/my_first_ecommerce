import email
from django import forms
from customers.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, min_length=5, required=True)
    email = forms.EmailField(max_length=100, min_length=10, required=True)
    password = forms.CharField(max_length=50, min_length=10, required=True)

    # Validaciones de formulario
    # Siempre nombrar las validaciones iniciando con "clean_[fieldname]()"
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El username ya se ha registrado')
        else:
            return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya se ha registrado')
        else:
            return email
    
    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password')
            )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, min_length=5, required=True)
    password = forms.CharField(max_length=50, min_length=5, required=True)

