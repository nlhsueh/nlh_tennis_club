from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20, 
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    password = forms.CharField(
        max_length=20, 
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
