from django.contrib import admin
from cart.models import CartItemModel, CartModel
# Register your models here.


class CartItemModelAdmin(admin.ModelAdmin):

    class Meta:
        model = CartItemModel
        list_display = ("cart", "quantity", "updated_date", "created_date")


class CartModelAdmin(admin.ModelAdmin):
    class Meta:
        model = CartModel
        list_display = ("user", "created_date", "updated_date")


admin.site.register(CartItemModel, CartItemModelAdmin)
admin.site.register(CartModel, CartModelAdmin)
