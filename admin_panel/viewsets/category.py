from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from products.models import Category


class CategoryList(generic.ListView):
    # queryset
    # model

    # template_name

    queryset = Category.objects.filter(parent__isnull=True)
    
    # prefetch_related(
    #     'features').annotate(
    #         published_features_count=Count('features',filter=Q(features__published=True)),
    #         all_features_count=Count('features'),
    #     ).all().order_by("-priority")

    
    template_name = "admin-panel/pages/category.html"
    ordering = ["id"]
    paginate_by = 10

    def get_queryset(self):
        # Request information is found here
        query_params = self.request.GET

        if parent_pk := query_params.get("parent"):
            return Category.objects.filter(parent__pk=parent_pk)
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        return data

class CategoryCreate(generic.CreateView):
    # queryset
    # model

    # template_name
    # fields

    model = Category
    template_name = "admin-panel/forms/form.html"
    fields = "__all__"

    success_url = reverse_lazy("admin-categories")

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        
        data.update(
            title = "Create Category",
            redirect_url=self.success_url,
        )
        return data

   

    
class CategoryEdit(generic.UpdateView):
    # queryset
    # model

    # template_name
    # fields

    model = Category
    template_name = "admin-panel/forms/form.html"
    fields = "__all__"

    success_url = reverse_lazy("admin-categories")

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)

        data.update(
            title = "Edit Category ? ",
            show_object = False,
            redirect_url=self.success_url,

        )
 
        return data


class CategoryDelete(generic.DeleteView):

    # queryset
    # model

    # template_name
    # fields

    model = Category
    template_name = "admin-panel/forms/form.html"
    success_url = reverse_lazy("admin-categories")

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)

        data.update(
            title = "Delete This Category Object ? ",
            show_object = True,
            redirect_url=self.success_url,
        )
 
        return data

        

