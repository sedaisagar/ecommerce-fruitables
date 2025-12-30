from django.db import models

from utils.models import CommonModel
from django.utils.text import slugify


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

# Fruits -- Parent
    # Apple -- First Child

# Vegetables -- Parent
    # Cauliflower -- First Child

# Electronics -- Parent
    # Home Appliances -- First Child
        # Refrigirator -- Second Child
        # Washing Machine -- Second Child

