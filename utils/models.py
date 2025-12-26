from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) # automatically caputres created dt
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CommonModel(BaseModel):   

    published = models.BooleanField()
    priority = models.PositiveIntegerField(default=0)


    class Meta:
        abstract = True


