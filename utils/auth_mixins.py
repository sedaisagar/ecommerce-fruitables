from django.contrib.auth.mixins import AccessMixin

from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.shortcuts import redirect

from django.http import HttpRequest

class AdminLoginRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        request : HttpRequest = request

        if request.user.is_authenticated and not request.user.is_anonymous:
            role = request.user.role
            if request.user.is_superuser:
                role = "ADMIN"
            match role:
                case "ADMIN":
                    return super().dispatch(request, *args, **kwargs)
                case _:
                    return redirect("client-dash")
        else:
            return self.handle_no_permission()