from typing import Any
from django.shortcuts import render
from django.views.generic import (
    View, 
    ListView,
    DetailView,
)
from .models import ProductModel,ProductStatusType,ProductCategoryModel,WishlistProductModel
from django.core.exceptions import FieldError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from review.models import ReviewModel,ReviewStatusType
from django.core.cache import cache
from django.core import serializers

# Create your views here.


class ShopProductGridView(ListView):
    template_name = 'shop/product_grid.html'
    paginate_by = 9

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        cache_key = "grid_view_model"
        cached_data = cache.get(cache_key)

        if not cached_data:
            print("Cache miss - Querying database")
            queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)
            # Serialize the queryset to JSON
            serialized_data = serializers.serialize('json', queryset)
            cache.set(cache_key, serialized_data, timeout=60*15)  # Cache for 15 minutes
        else:
            print("Cache hit")
            # Deserialize the JSON data to a queryset
            queryset = [obj.object for obj in serializers.deserialize('json', cached_data)]

        # Apply additional filters if present
        queryset = ProductModel.objects.filter(pk__in=[obj.pk for obj in queryset])

        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title__icontains=search_q)
        if category_id := self.request.GET.get("category_id"):
            queryset = queryset.filter(category__id=category_id)
        if min_price := self.request.GET.get("min_price"):
            queryset = queryset.filter(price__gte=min_price)
        if max_price := self.request.GET.get("max_price"):
            queryset = queryset.filter(price__lte=max_price)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if context data is in cache
        cache_key_total_items = "total_items"
        cache_key_categories = "product_categories"

        total_items = cache.get(cache_key_total_items)
        if total_items is None:
            total_items = self.get_queryset().count()
            cache.set(cache_key_total_items, total_items, timeout=60*15)  # Cache for 15 minutes

        categories = cache.get(cache_key_categories)
        if categories is None:
            categories = list(ProductCategoryModel.objects.all())
            cache.set(cache_key_categories, categories, timeout=60*15)  # Cache for 15 minutes

        context["total_items"] = total_items
        context["categories"] = categories

        return context

class ShopProductDetailView(DetailView):
    template_name = 'shop/product_single.html'
    queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["is_wished"] = WishlistProductModel.objects.filter(
            user=self.request.user, product__id=product.id).exists() if self.request.user.is_authenticated else False
        reviews = ReviewModel.objects.filter(product=product,status=ReviewStatusType.accepted.value)
        context["reviews"] = reviews
        total_reviews_count =reviews.count()
        context["reviews_count"] = {
            f"rate_{rate}": reviews.filter(rate=rate).count() for rate in range(1, 6)
        }
        if total_reviews_count != 0:
            context["reviews_avg"] = {
                f"rate_{rate}": round((reviews.filter(rate=rate).count()/total_reviews_count)*100,2) for rate in range(1, 6)
            }
        else:
            context["reviews_avg"] = {f"rate_{rate}": 0 for rate in range(1, 6)}
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.product_images.prefetch_related()
        return obj
    

class AddOrRemoveWishlistView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get("product_id")
        message = ""
        if product_id:
            try:
                wishlist_item = WishlistProductModel.objects.get(
                    user=request.user, product__id=product_id)
                wishlist_item.delete()
                message = "محصول از لیست علایق حذف شد"
            except WishlistProductModel.DoesNotExist:
                WishlistProductModel.objects.create(
                    user=request.user, product_id=product_id)
                message = "محصول به لیست علایق اضافه شد"

        return JsonResponse({"message": message})
