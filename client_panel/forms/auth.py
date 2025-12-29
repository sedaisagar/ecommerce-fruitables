from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

class ForgotPwdForm(forms.Form):
    email = forms.EmailField()

class SetPwdForm(forms.Form):
    otp = forms.DecimalField(max_digits=6, decimal_places=0)
    password = forms.CharField()