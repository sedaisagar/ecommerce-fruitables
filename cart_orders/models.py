from django.db import models

from products.models import Products
from users.models import User
from utils.models import BaseModel

class UserCart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name="cart")
    order_notes = models.TextField()

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

    @property
    def total(self):
        return self.price * self.quantity



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


    class Meta:
        db_table = "shipping_billing_address"




class UserOrder(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name="orders")
    order_notes = models.TextField()

    class Meta:
        db_table = "user_order"


class OrderItems(BaseModel):
    order = models.ForeignKey(UserOrder, on_delete=models.CASCADE, related_name="order_items")
    #
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    class  Meta:
        db_table = "order_items"

    @property
    def total(self):
        return self.price * self.quantity


class PaymentDetails(BaseModel):
    PAYMENT_METHODS = (
        ("khalti", "Khalti"),
        ("esewa", "Esewa"),
        ("cod", "Cash On Delivery"),
    )

    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )

    cart = models.OneToOneField(UserCart, on_delete=models.CASCADE, related_name="payment_details", null=True, blank=True)
    order = models.OneToOneField(UserOrder, on_delete=models.CASCADE, related_name="payment_details", null=True, blank=True)


    payment_method = models.CharField(max_length=6, choices=PAYMENT_METHODS)
    payment_id = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=9, choices=PAYMENT_STATUS, default="pending")
    extra_data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "payment_details"

# Pre Save / Post Save Signals
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

@receiver(pre_save, sender=PaymentDetails)
def receive_payment_details_pre_save(sender, **kwargs):
    print(vars(kwargs['instance']))

@receiver(post_save, sender=PaymentDetails)
def receive_payment_details_post_save(sender, **kwargs):
    print(vars(kwargs['instance']))






# User - X

    # 1 Cart

        # Item A (1, 21)
        # Item B (2, 250)
        # .....
        # Item N (N, M)


        # Payment Process

        # 1. Initiate Payment -> 2. User Pays for the Cart -> 3. Payment Verification -> 4. Convert Cart to Order