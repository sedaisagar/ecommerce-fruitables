import json
import random
from django.shortcuts import redirect
from django.views import generic

from cart_orders.models import OrderItems, PaymentDetails, ShippingBillingAddress, UserCart, PurchaseItems, UserOrder
from client_panel.forms.cart import CartAddForm, ShippingBillingForm
from products.models import Products

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F,Sum

from django.conf import settings

import requests

class ClientDashBoardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "client-panel/dashboard/index.html"

    
    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        order = UserOrder.objects.filter(user=self.request.user).prefetch_related("order_items","payment_details") # prefetch related
        data["orders"] = order
        return data

class ClientPaymentVerifyView(generic.TemplateView):
    template_name = "client-panel/dashboard/payment-verify.html"

    def handle_khalti_payment_verification(self, request):
        params = request.GET.dict()
        pidx = params.get("pidx", "")
        purchase_order_id = params.get("purchase_order_id", "")

        payment_details = PaymentDetails.objects.filter(payment_id=purchase_order_id).first()
        
        if not payment_details:
            # fallback page
            return redirect("client-dash")
        
        url = settings.KHALTI_API
        verify_url = url + "epayment/lookup/"
        secret_key = settings.KHALTI_LIVE_SECRET_KEY

        headers = {
            "Authorization": f"Key {secret_key}",  
             'Content-Type': 'application/json',
        }  

        payload = {
            "pidx": pidx
        }

        response = requests.request("POST", verify_url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200: # Sucess Case 
            data = response.json()
            status = data.get("status")
            match status:
                case "Completed":
                    payment_details.status = "completed"
                    
                    # Order place
                    cart = payment_details.cart
                    if cart:
                        user_order = UserOrder.objects.create(
                            user = cart.user,
                            order_notes = cart.order_notes or ""
                        )
                        purchase_items = cart.purchase_items.all()
                        order_items_bulk = [] # 100 items to be created
                        for item in purchase_items:
                            order_item =  OrderItems(
                                order = user_order,
                                product = item.product,
                                quantity = item.quantity,
                                price = item.price,
                            )
                            order_items_bulk.append(order_item)
                        OrderItems.objects.bulk_create(order_items_bulk)

                        # Clear order notes after creating order
                        cart.order_notes = ""
                        cart.save(update_fields=["order_notes"])

                        purchase_items.delete() # Clear Purchase Items After Order Created

                        payment_details.order = user_order
                        payment_details.cart = None
                        payment_details.extra_data = data
                        payment_details.save(update_fields=["status", "order", "cart", "extra_data"])
    

                case _:
                    # fallback page
                    return redirect("client-dash")
        
        return redirect("client-dash")
        
    def get(self, request, *args, **kwargs):
        # Handle Payment Verification Logic Here
        return self.handle_khalti_payment_verification(request)
    
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

            PaymentDetails.objects.create(
                cart = cart,
                order = None,
                payment_method = "khalti",
                payment_id = payload.get("purchase_order_id"),
                amount = cart_total,
                status = "pending",
                extra_data = {}
            )

            return redirect(checkout_url)

    def handle_cod(self, request, context_data):
        cart : UserCart = context_data.get("cart")
        purchase_items  = context_data.get("items")

        user_order = UserOrder.objects.create(
            user = cart.user,
            order_notes = cart.order_notes or ""
        )
        order_items_bulk = [] # 100 items to be created
        for item in purchase_items:
            order_item =  OrderItems(
                order = user_order,
                product = item.product,
                quantity = item.quantity,
                price = item.price,
            )
            order_items_bulk.append(order_item)
        OrderItems.objects.bulk_create(order_items_bulk)

        # Clear order notes after creating order
        cart.order_notes = ""
        cart.save(update_fields=["order_notes"])

        purchase_items.delete() # Clear Purchase Items After Order Created

        PaymentDetails.objects.create(
            cart = None,
            order = user_order,
            payment_method = "cod",
            payment_id = f"COD-{user_order.pk}-{random.randint(100000,999999)}",
            amount = context_data.get("cart_total", 0),
            status = "completed",
            extra_data = {"notes": "Cash on Delivery selected by user."}
        )



    def post(self, request, *args, **kwargs):
        # Handle Checkout Logic Here
        context_data = self.get_context_data(**kwargs)
        cart_total = context_data.get("cart_total", 0)
        cart : UserCart = context_data.get("cart")
        if not cart_total:
            return redirect("shop-page")
        
        # Update order notes to cart instance
        order_notes = request.POST.get("order_notes", "")
        cart.order_notes = order_notes
        cart.save(update_fields=["order_notes"])
        
        payment_method = request.POST.get("payment_method", "")

        form = ShippingBillingForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            shipping_address, created = ShippingBillingAddress.objects.update_or_create(
                user=request.user,
                defaults = data
            )

            # Proceed to Payment Gateway Integration
            match payment_method:
                case "khalti":
                    response =  self.handle_khalti_payment(request, cart, cart_total)
                    
                    if response:
                        return response
                    
                case "esewa":
                    pass
                case "cod":
                    self.handle_cod(request, context_data)

        return redirect("client-dash")
    
# ACID - Atomicity, Consistency, Isolation, Durability