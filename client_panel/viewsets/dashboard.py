from django.shortcuts import redirect
from django.views import generic

from cart_orders.models import UserCart, PurchaseItems
from client_panel.forms.cart import CartAddForm
from products.models import Products

class ClientDashBoardView(generic.TemplateView):
    template_name = "client-panel/dashboard/index.html"

    

class ClientCartView(generic.TemplateView):
    template_name = "client-panel/dashboard/cart.html"

    def handle_cart_add_action(self, data ): # = {"product":None, "quantity":None}
        user = self.request.user
        product : Products = data.get("product")
        quantity = data.get("quantity")

        # UserCart.objects.get_or_create(user=user, defaults={"a":"adsasd", "b":"asdasd"})
        cart, _ = UserCart.objects.get_or_create(user=user)

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
    

class ClientCheckOutView(generic.TemplateView):
    template_name = "client-panel/dashboard/checkout.html"

    