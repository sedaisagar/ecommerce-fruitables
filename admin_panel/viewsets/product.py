from django import forms
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

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
    template_name = "admin-panel/forms/form.html"
    fields = "__all__"
    # fields = ["parent", "name", "slug", "published", "priority"]

    success_url = reverse_lazy("admin-products")

    # def get_success_url(self):
    #     url =  super().get_success_url()
    #     query_params = self.request.GET
    #     if parent_pk := query_params.get("parent"):
    #         url = f"{url}?parent={parent_pk}"
    #     return url 

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        # query_params = self.request.GET

        # if parent_pk := query_params.get("parent"):
        #     data.update(parent=parent_pk)

        data.update(
            title = "Create Products",
            redirect_url=self.success_url,
        )
        return data
    
    def get_initial(self):
        data = super().get_initial()

        # query_params = self.request.GET
        # if parent_pk := query_params.get("parent"):
        #     data['parent'] = parent_pk
        return data

    def get_form(self, form_class = None):
        print("GET form")
        form = super().get_form(form_class)
        form.fields['description'].widget = TinyMCE(attrs={'cols': 80, 'rows': 30})

        # form.fields['parent'] = forms.CharField(widget=forms.HiddenInput())

        # form.fields['parent'].label.title = ""
        # form.fields['parent'].widget.attrs.update( {"style":"display:none"})
        
        return form

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
  
class ProductsDetail(generic.DetailView):
    # queryset
    # model

    # template_name
    # fields

    model = Products
    template_name = "admin-panel/pages/product-detail.html"
    
    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        # self.request.build_absolute_uri()
        return data

    
class ProductsEdit(generic.UpdateView):
    # queryset
    # model

    # template_name
    # fields

    model = Products
    template_name = "admin-panel/forms/form.html"
    fields = "__all__"
    # fields = ["name", "slug", "published", "priority"]


    success_url = reverse_lazy("admin-products")

    """
    def form_valid(self, form):
        # If the form is valid, redirect to the supplied URL.
        super().form_valid(form)
        return redirect("admin-categories")
    """

    # def get_success_url(self):
    #     url =  super().get_success_url()
    #     query_params = self.request.GET
    #     if parent_pk := query_params.get("parent"):
    #         url = f"{url}?parent={parent_pk}"
    #     return url 

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)

        # query_params = self.request.GET

        # if parent_pk := query_params.get("parent"):
            # data.update(parent=parent_pk)

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

        # form.fields['parent'] = forms.CharField(widget=forms.HiddenInput())

        # form.fields['parent'].label.title = ""
        # form.fields['parent'].widget.attrs.update( {"style":"display:none"})
        
        return form


class ProductsDelete(generic.DeleteView):

    # queryset
    # model

    # template_name
    # fields

    model = Products
    template_name = "admin-panel/forms/form.html"
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

        

