from django.db import models

from utils.models import CommonModel
from django.utils.text import slugify
from django.urls import reverse_lazy

from utils.uri_builder import UriUtils

class Category(CommonModel):
    name = models.CharField(max_length=45)
    slug = models.SlugField(null=True, blank=True, unique=True)

    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="children", null=True,blank=True)

    class Meta:
        db_table = "categories"


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url_for_edit(self):
        rel_url= reverse_lazy("admin-categories-edit", kwargs = {'pk':self.pk}) # just str form of url
        return UriUtils.build_custom_uri(rel_url)

    def get_absolute_url_for_delete(self):
        rel_url= reverse_lazy("admin-categories-delete", kwargs = {'pk':self.pk})
        return UriUtils.build_custom_uri(rel_url)

    def get_absolute_url(self):
        rel_url= reverse_lazy("admin-categories-detail", kwargs = {'pk':self.pk})
        return UriUtils.build_custom_uri(rel_url)

# Fruits -- Parent
    # Apple -- First Child

# Vegetables -- Parent
    # Cauliflower -- First Child

# Electronics -- Parent
    # Home Appliances -- First Child
        # Refrigirator -- Second Child
        # Washing Machine -- Second Child

