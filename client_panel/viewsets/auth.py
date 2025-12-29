import random
from django.views import generic
from django.shortcuts import redirect

from client_panel.forms.auth import ForgotPwdForm, LoginForm
from django.contrib.auth import authenticate , login, logout
from django.contrib.auth.hashers import make_password

from users.models import User, UserOtp


class LoginPage(generic.TemplateView):
    template_name = "admin-panel/pages/login.html"

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            return redirect("admin-dashboard")

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            auth_ok = authenticate(request, **data)
            if auth_ok:
                login(request, auth_ok)
                return redirect("admin-dashboard")
        return super().get(request, *args, **kwargs)

class RegisterPage(generic.TemplateView):
    template_name = "admin-panel/pages/register.html"

    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data["username"] = data["email"]
            
            data["password"] = make_password(data["password"]) # Hashing password
            User.objects.create(**data)
            return redirect("login-page")

        return super().get(request, *args, **kwargs)

class LogoutPage(generic.TemplateView):
    template_name = "admin-panel/pages/logout.html"

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect("login-page")

        

class ForgotPwdPage(generic.TemplateView):
    template_name = "admin-panel/pages/forgot-password.html"

    def post(self, request, *args, **kwargs):
        form = ForgotPwdForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.filter(**data) # QS / queryset

            if user.exists(): # If some data is present under our cond
                user = user.first() # getting first item
                
                otp = UserOtp.objects.filter(user=user)
                if otp.exists():
                    otp.delete()
                    
                random_otp = random.randint(0,999999)
                UserOtp.objects.create(user = user, otp=random_otp)

                # Send email to respective user with the otp

                # 
        return super().get(request, *args, **kwargs)


        