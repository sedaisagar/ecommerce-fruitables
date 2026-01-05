from django.views import generic

from products.models import Products


class HomePage(generic.TemplateView):
    template_name = "client-panel/index.html"

class ShopPage(generic.ListView):
    template_name = "client-panel/shop.html"
    queryset = Products.objects.all()
    paginate_by = 9

class ShopDetailPage(generic.DetailView):
    template_name = "client-panel/shop-detail.html"
    model = Products
    # query_pk_and_slug = True  