from django.views import generic

from utils.auth_mixins import AdminLoginRequiredMixin

class AdminDashBoardPage(AdminLoginRequiredMixin,generic.TemplateView):
    template_name = "admin-panel/pages/index.html"


