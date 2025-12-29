from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class AdminDashBoardPage(LoginRequiredMixin,generic.TemplateView):
    template_name = "admin-panel/pages/index.html"


