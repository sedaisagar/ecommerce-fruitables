from django.views import generic


class HomePage(generic.TemplateView):
    template_name = "client-panel/index.html"

class ShopPage(generic.TemplateView):
    template_name = "client-panel/shop.html"