from django.views import generic

from products.models import Products


class HomePage(generic.TemplateView):
    template_name = "client-panel/index.html"

class ShopPage(generic.TemplateView):
    template_name = "client-panel/shop.html"

class ShopDetailPage(generic.DetailView):
    template_name = "client-panel/shop-detail.html"
    model = Products
    # query_pk_and_slug = True  