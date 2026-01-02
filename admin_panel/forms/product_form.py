from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit, HTML

from products.models import Category, Products
from tinymce.widgets import TinyMCE

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = [
            "category", "name", "slug",
            "market_price", "price",
            "short_description", "image", "priority",
            "published",
            "is_featured", "is_organic", "is_fresh",
            "is_on_sales", "is_on_discount", "is_expired",
            "description",
        ]
        widgets = {"description":TinyMCE(), "short_description":forms.Textarea(attrs={"rows":4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        self.fields["category"].choices = [
            ("", "---------")
        ] + self.get_category_choices(categories)

        self.helper = FormHelper(self)
        self.helper.form_method = "post"

        self.helper.layout = Layout(

            ## Row 1
            Row(
                Column("category", css_class="col-md-4"),
                Column("name", css_class="col-md-4"),
                Column("slug", css_class="col-md-4"),
            ),

            ## Row 2
            Row(
                Column("image", css_class="col-md-8"),
                Column("priority", css_class="col-md-4"),
            
            ),
            Row(
                Column("market_price", css_class="col-md-6"),
                Column("price", css_class="col-md-6"),
            ),

            ## Row 3
            Row(
                Column("short_description", css_class="col-md-12"),
            ),
            
            ## Feature flags (checkboxes)
            Row(
                Column(HTML("<h1>Flags</h1>"), css_class="col-md-12"),
                Column(HTML("<hr/>"), css_class="col-md-12"),
                Column("published", css_class="col-md-3"),
                Column("is_featured", css_class="col-md-3"),
                Column("is_organic", css_class="col-md-3"),
                Column("is_fresh", css_class="col-md-3"),
                Column("is_on_sales", css_class="col-md-3"),
                Column("is_on_discount", css_class="col-md-3"),
                Column("is_expired", css_class="col-md-3"),
                Column(HTML("<hr/>"), css_class="col-md-12"),
            ),
            ## Description
            Row(
                Column("description", css_class="col-12"),
            ),

            Submit("submit", "Submit", css_class="mt-3"),
        )

    def get_category_choices(self, categories, parent=None, level=0):
        choices = []
        for category in categories.filter(parent=parent):
            prefix = "——" * level
            choices.append((category.id, f"{prefix}{category.name}"))
            choices.extend(
                self.get_category_choices(categories, parent=category, level=level + 1)
            )
        return choices