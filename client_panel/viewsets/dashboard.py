from django.shortcuts import redirect
from django.views import generic

from cart_orders.models import UserCart, PurchaseItems
from client_panel.forms.cart import CartAddForm
from products.models import Products

from django.contrib.auth.mixins import LoginRequiredMixin

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

        return data

class ClientCheckOutView(LoginRequiredMixin, generic.TemplateView):
    template_name = "client-panel/dashboard/checkout.html"

    