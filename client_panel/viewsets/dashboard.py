from django.views import generic

class ClientDashBoardView(generic.TemplateView):
    template_name = "client-panel/dashboard/index.html"

    

class ClientCartView(generic.TemplateView):
    template_name = "client-panel/dashboard/cart.html"

    

class ClientCheckOutView(generic.TemplateView):
    template_name = "client-panel/dashboard/checkout.html"

    