from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

class ForgotPwdForm(forms.Form):
    email = forms.EmailField()