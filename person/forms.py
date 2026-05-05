from django import forms


class LoginForm(forms.Form):
    Username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'username-in',
        'placeholder': 'نام کاربری خود را وارد کنید...'
    }))
    Password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'password-in',
        'placeholder': 'گذرواژه خود را وارد کنید...',
        'type': 'password'
    }))
