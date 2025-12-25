from django.views import generic


class AdminDashBoardPage(generic.TemplateView):
    template_name = "admin-panel/index.html"