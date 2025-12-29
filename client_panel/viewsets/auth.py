import random
from django.views import generic
from django.shortcuts import redirect

from client_panel.forms.auth import ForgotPwdForm, LoginForm, SetPwdForm
from django.contrib.auth import authenticate , login, logout
from django.contrib.auth.hashers import make_password

from users.models import User, UserOtp
from django.core.mail import send_mail
from core import settings

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
                send_mail(
                    "Your Password Reset OTP is >>",
                    f"{random_otp}",
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                # 
                # redirect to otp and pwd set screen
                return redirect("spwd-page")

        return super().get(request, *args, **kwargs)


class SetPwdPage(generic.TemplateView):
    template_name = "admin-panel/pages/set-password.html"

    def post(self, request, *args, **kwargs):
        form = SetPwdForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # otp = data["otp"] # issue may be caused
            otp = data.get("otp")

            otp = UserOtp.objects.filter(otp=otp)

            if otp.exists(): # If some data is present under our cond
                otp = otp.first() # getting first item
                
                user = otp.user

                password = data.get("password")
                user.set_password(password) # object password assigned but not saved in db
                user.save() # acutally saved in db

                otp.delete()

            print("<<<<<<<<<<<<< Everything Ok >>>>>>>>>>>")
            return redirect("login-page")

        print("<<<<<<<<<<<<< Nothing Ok >>>>>>>>>>>")
        return redirect("login-page")


        