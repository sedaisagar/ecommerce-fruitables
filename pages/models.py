from django.db import models
from django.utils.text import slugify
from utils.models import CommonModel

# Create your models here.
class DynamicPages(CommonModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, unique=True)
    description = models.TextField()

    class Meta:
        db_table = "dy_pages"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)            
        super().save(*args, **kwargs)
