from django.db import models

from products.models import Products
from users.models import User
from utils.models import BaseModel

class UserCart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name="cart")

    class Meta:
        db_table = "user_cart"


class PurchaseItems(BaseModel):
    cart = models.ForeignKey(UserCart, on_delete=models.CASCADE, related_name="purchase_items")
    #
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="purchase_items")
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    class  Meta:
        db_table = "purchase_items"


class ShippingBillingAddress(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shipping_billing_address")

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    email = models.EmailField()

    order_notes = models.TextField()


    class Meta:
        db_table = "shipping_billing_address"

# User - X

    # 1 Cart

        # Item A (1, 21)
        # Item B (2, 250)
        # .....
        # Item N (N, M)