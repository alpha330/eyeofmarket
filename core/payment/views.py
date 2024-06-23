from django.shortcuts import render
from django.views.generic import View
from .models import PaymentModel, PaymentStatusType
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from .zarinpal_client import ZarinPalSandbox
from .parspay_client import ParsPaySandBox
from order.models import OrderModel, OrderStatusType,OrderItemModel
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from cart.validators import ProductCountsManagement

# Create your views here.


class PaymentVerifyView(View):
    
    def get(self, request, *args, **kwargs):
        authority_id = request.GET.get("Authority")
        status = request.GET.get("Status")

        payment_obj = get_object_or_404(
            PaymentModel, authority_id=authority_id)
        order = OrderModel.objects.get(payment=payment_obj)
        order_items = OrderItemModel.objects.filter(order=order)
        zarin_pal = ZarinPalSandbox() 
        response = zarin_pal.payment_verify(
            int(payment_obj.amount), payment_obj.authority_id)
        ref_id = response["RefID"]
        status_code = response["Status"]

        payment_obj.ref_id = ref_id
        payment_obj.response_code = status_code
        payment_obj.status = PaymentStatusType.success.value if status_code in {
            100, 101} else PaymentStatusType.failed.value
        payment_obj.response_json = response
        payment_obj.save()

        order.status = OrderStatusType.success.value if status_code in {
            100, 101} else OrderStatusType.failed.value
        order.save()
        if status_code in {100, 101}:
            return redirect(reverse_lazy("order:completed"))
        else:
            for item in order_items:
                quantity = item.quantity
                product_id = item.product.id
                ProductCountsManagement.return_to_stock(product_id=product_id, quantity=quantity)
            return redirect(reverse_lazy("order:failed"))
    
class PaymentVerifyParsPayView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request.POST.get("status") in {"100","101"}:
            authority_id = request.POST.get("payment_id")
            status = request.POST.get("status")
            receipt_number = request.POST.get("receipt_number")
            payment_obj = get_object_or_404(
                PaymentModel, authority_id=authority_id)
            order = OrderModel.objects.get(payment=payment_obj)
            currency = payment_obj.currency
            parspay = ParsPaySandBox()
            response = parspay.payment_verify(
                amount=int(payment_obj.amount),receipt_number=receipt_number,currency=currency)
            if response["status"] == "SUCCESSFUL":
                payment_obj.ref_id = authority_id
                payment_obj.response_code = status
                payment_obj.recipt_code = int(receipt_number)
                payment_obj.status = PaymentStatusType.success.value
                payment_obj.response_json = response
                payment_obj.save()
                order.status = OrderStatusType.success.value
                order.save()
                messages.success(self.request,response["message"])
                return redirect(reverse_lazy("order:completed"))
            else:
                payment_obj.ref_id = authority_id
                payment_obj.response_code = status
                payment_obj.recipt_code = 0
                payment_obj.status = PaymentStatusType.failed.value
                payment_obj.response_json = response 
                payment_obj.save()
                order.status = OrderStatusType.failed.value
                order.save() 
                messages.error(self.request,response["message"])
                return redirect(reverse_lazy("order:failed"))
        else:
            authority_id = request.POST.get("payment_id")
            status = request.POST.get("status")
            payment_obj = get_object_or_404(
                PaymentModel, authority_id=authority_id)
            order = OrderModel.objects.get(payment=payment_obj)
            parspay = ParsPaySandBox() 
            response_inquery = parspay.payment_inquery(amount=int(payment_obj.amount),payment_id=payment_obj.authority_id)
            payment_obj.ref_id = authority_id
            payment_obj.response_code = status
            payment_obj.recipt_code = 0
            payment_obj.status = PaymentStatusType.failed.value
            payment_obj.response_json = response_inquery
            payment_obj.save()
            order.status = OrderStatusType.failed.value
            order.save() 
            return redirect(reverse_lazy("order:failed"))