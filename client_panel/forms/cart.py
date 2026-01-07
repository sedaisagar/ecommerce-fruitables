from django import forms

from cart_orders.models import PurchaseItems, ShippingBillingAddress

class CartAddForm(forms.ModelForm):
    class Meta:
        model = PurchaseItems
        fields = ["product", "quantity"]

class ShippingBillingForm(forms.ModelForm):
    class Meta:
        model = ShippingBillingAddress
        # fields = "__all__"
        fields = [
            "first_name",
            "last_name",
            "company_name",
            "address",
            "city",
            "country",
            "zip_code",
            "mobile",
            "email",
            "order_notes",
        ]
