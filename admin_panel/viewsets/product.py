from django import forms
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from admin_panel.forms.product_form import ProductForm
from products.models import Products
from tinymce.widgets import TinyMCE

class ProductsList(generic.ListView):
    # queryset
    # model

    # template_name

    queryset = Products.objects.filter()
    
    # prefetch_related(
    #     'features').annotate(
    #         published_features_count=Count('features',filter=Q(features__published=True)),
    #         all_features_count=Count('features'),
    #     ).all().order_by("-priority")

    
    template_name = "admin-panel/pages/product.html"
    ordering = ["id"]
    paginate_by = 10

    def get_queryset(self):
        # Request information is found here

        # query_params = self.request.GET
        # if parent_pk := query_params.get("parent"):
        #     return Products.objects.filter(parent__pk=parent_pk)

        return super().get_queryset()

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        # query_params = self.request.GET
        # if parent_pk := query_params.get("parent"):
        #     data.update(parent=parent_pk)
        return data

class ProductsCreate(generic.CreateView):
    # queryset
    # model

    # template_name
    # fields

    model = Products
    template_name = "admin-panel/forms/dynamic-form.html"
    form_class = ProductForm

    success_url = reverse_lazy("admin-products")

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        
        data.update(
            title = "Create Products",
            redirect_url=self.success_url,
        )
        return data
    
    
class ProductsDetail(generic.DetailView):
    model = Products
    template_name = "admin-panel/pages/product-detail.html"
    
    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        return data

    
class ProductsEdit(generic.UpdateView):
    model = Products
    template_name = "admin-panel/forms/dynamic-form.html"
    # fields = [
    #     "category",
    #     "name",
    #     "slug",
    #     "market_price",
    #     "price",
    #     "short_description",
    #     "image",
    #     "description",
    #     "priority",
    #     "published",
    #     "is_featured",
    #     "is_organic",
    #     "is_fresh",
    #     "is_on_sales",
    #     "is_on_discount",
    #     "is_expired",
    # ]
    form_class = ProductForm


    success_url = reverse_lazy("admin-products")

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        data.update(
            title = "Edit Products ? ",
            show_object = False,
            redirect_url=self.success_url,

        )
 
        return data

    def get_form(self, form_class = None):
        print("GET form")
        form = super().get_form(form_class)
        form.fields['description'].widget = TinyMCE(attrs={'cols': 80, 'rows': 30})
        return form


class ProductsDelete(generic.DeleteView):

    # queryset
    # model

    # template_name
    # fields

    model = Products
    template_name = "admin-panel/forms/dynamic-form.html"
    success_url = reverse_lazy("admin-products")
    
    # def get_success_url(self):
    #     url =  super().get_success_url()
    #     query_params = self.request.GET
    #     if parent_pk := query_params.get("parent"):
    #         url = f"{url}?parent={parent_pk}"
    # #     return url 

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)

        # query_params = self.request.GET

        # if parent_pk := query_params.get("parent"):
            # data.update(parent=parent_pk)

        data.update(
            title = "Delete This Products Object ? ",
            show_object = True,
            redirect_url=self.success_url,
        )
 
        return data

        

