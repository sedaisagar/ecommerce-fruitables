from django.db import models

from utils.models import CommonModel
from django.utils.text import slugify

class Category(CommonModel):
    name = models.CharField(max_length=45)
    slug = models.SlugField(null=True, blank=True, unique=True)

    class Meta:
        db_table = "categories"


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            
        super().save(*args, **kwargs)
