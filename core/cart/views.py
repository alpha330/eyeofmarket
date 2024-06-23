from typing import Any
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import JsonResponse
from shop.models import ProductModel, ProductStatusType
from django.contrib import messages
from .cart import CartSession
from .validators import ProductCountsManagement

class SessionAddProductView(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        product = ProductModel.objects.filter(id=product_id, status=ProductStatusType.publish.value)
        product_stock = ProductModel.objects.get(id=product_id,status=ProductStatusType.publish.value)
        if product_id and product.exists() and product_stock.stock > 0:
            cart.add_product(product_id)
            ProductCountsManagement.stock_updates(product_id=product_id,quantity=1)
        else:
            print("موجود نیست")
            messages.error(self.request,"در انبار موجود نمی باشد")
            return JsonResponse({"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()})
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        messages.success(self.request,"به سبد اضافه شد")
        return JsonResponse({"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()})


class SessionRemoveProductView(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")
        print(quantity)
        if product_id and quantity:
            cart.remove_product(product_id)
            ProductCountsManagement.return_to_stock(product_id=product_id,quantity=int(quantity))
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        messages.success(self.request,"از سبدحذف شد")
        return JsonResponse({"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()})


class SessionUpdateProductQuantityView(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")
        
        if product_id and quantity:
            cart.update_product_quantity(product_id, quantity)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse({"cart": cart.get_cart_dict(), "total_quantity": cart.get_total_quantity()})


class CartSummaryView(TemplateView):
    template_name = "cart/cart-summary.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        cart = CartSession(self.request.session)
        cart_items = cart.get_cart_items()
        context["cart_items"] = cart_items
        context["total_quantity"] = cart.get_total_quantity()
        context["total_payment_price"] = cart.get_total_payment_amount()
        return context