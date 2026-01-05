from django import forms

from cart_orders.models import PurchaseItems

class CartAddForm(forms.ModelForm):
    class Meta:
        model = PurchaseItems
        fields = ["product", "quantity"]
