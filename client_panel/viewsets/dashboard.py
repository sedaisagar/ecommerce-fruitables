import json
import random
from django.shortcuts import redirect
from django.views import generic

from cart_orders.models import ShippingBillingAddress, UserCart, PurchaseItems
from client_panel.forms.cart import CartAddForm, ShippingBillingForm
from products.models import Products

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F,Sum

from django.conf import settings

import requests

class ClientDashBoardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "client-panel/dashboard/index.html"

    

class ClientCartView(LoginRequiredMixin, generic.TemplateView):
    template_name = "client-panel/dashboard/cart.html"

    def handle_cart_add_action(self, data ): # = {"product":None, "quantity":None}
        user = self.request.user
        product : Products = data.get("product")
        quantity = data.get("quantity")

        # UserCart.objects.get_or_create(user=user, defaults={"a":"adsasd", "b":"asdasd"})
        cart, _ = UserCart.objects.get_or_create(user=user)


        # Logic Here
        if quantity <= 0:
            PurchaseItems.objects.filter(cart= cart, product=product).delete()         
        else:
            purchase_item, created = PurchaseItems.objects.get_or_create(cart=cart, product=product, defaults=dict(quantity=quantity, price = product.price))
            if not created:
                purchase_item.quantity = quantity
                purchase_item.price = product.price
                purchase_item.save(update_fields=["quantity", "price"])

    def post(self,request, *args, **kwargs):
        form = CartAddForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            self.handle_cart_add_action(data) # handling cart add action            

        return redirect("client-cart")

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        cart = UserCart.objects.filter(user=self.request.user) # prefetch related
        if cart.exists():
            cart = cart.first()
            items = cart.purchase_items.all()
            data["items"] = items
            data["cart_total"] = items.aggregate(total=Sum(F("quantity")*F("price"))).get("total") or 0
        return data


# Model.objects.aggregate() # ->  Add, Sub, Mul, Div, Count, Avg, Max, Min

class ClientCheckOutView(LoginRequiredMixin, generic.TemplateView):
    template_name = "client-panel/dashboard/checkout.html"

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        cart = UserCart.objects.filter(user=self.request.user) # prefetch related
        if cart.exists():
            cart = cart.first()
            items = cart.purchase_items.all()
            data["items"] = items
            data["cart_total"] = items.aggregate(total=Sum(F("quantity")*F("price"))).get("total") or 0
            data["cart"] = cart
            data["address"] = ShippingBillingAddress.objects.filter(user=self.request.user).first()
            # breakpoint()
        return data
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context.get("cart_total", 0) <= 0:
            return redirect("shop-page")
        return self.render_to_response(context)
    
    def handle_khalti_payment(self, request, cart, cart_total):
        # Khalti Payment Integration
        url = settings.KHALTI_API
        initiate_url = url + "epayment/initiate/"
        secret_key = settings.KHALTI_LIVE_SECRET_KEY

        headers = {
            "Authorization": f"Key {secret_key}",  
             'Content-Type': 'application/json',
        }  

        payload = {
            "return_url": "http://localhost:8000/payment-verify/",
            "website_url": "http://localhost:8000/",
            "amount": float(cart_total) * 100,  # Amount in paisa
            "purchase_order_id": f"{cart.id}-{random.randint(1000,9999)}",
            "purchase_order_name": f"Ecommerce Payment - {cart.id} - by - {request.user.username}",
        }
        response = requests.request("POST", initiate_url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200: # Sucess Case 
            response_data = response.json()
            checkout_url = response_data.get("payment_url")
            return redirect(checkout_url)

    def post(self, request, *args, **kwargs):
        # Handle Checkout Logic Here
        data = self.get_context_data(**kwargs)
        cart_total = data.get("cart_total", 0)
        cart = data.get("cart")
        if not cart_total:
            return redirect("shop-page")
        
        form = ShippingBillingForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            shipping_address, created = ShippingBillingAddress.objects.update_or_create(
                user=request.user,
                defaults = data
            )

            # Proceed to Payment Gateway Integration
            return self.handle_khalti_payment(request, cart, cart_total)
        return redirect("client-dash")