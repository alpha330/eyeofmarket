from django.db.models.base import Model as Model
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from dashboard.admin.forms import *
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from shop.models import ProductModel, ProductCategoryModel
from django.core.exceptions import FieldError


class AdminProductGroupListView(LoginRequiredMixin, HasAdminAccessPermission, ListView):
    template_name = "dashboard/admin/product-group/product-group-list.html"
    paginate_by = 10
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)
    
    def get_queryset(self):
        queryset = ProductCategoryModel.objects.all()
        if search_q := self.request.GET.get("q"):
            queryset = queryset.filter(title=search_q)
        if order_by := self.request.GET.get("order_by"):
            try:
                queryset = queryset.order_by(order_by)
            except FieldError:
                pass
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_items"] = self.get_queryset().count()
        context["categories"] = ProductCategoryModel.objects.all()
        return context
    
class AdminProductGroupCreateView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, CreateView):
    template_name = "dashboard/admin/product-group/product-group-create.html"
    queryset = ProductModel.objects.all()
    form_class = ProductGroupForm
    success_message = "ایجاد گروه محصول با موفقیت انجام شد "

    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        return redirect(reverse_lazy("dashboard:admin:product-edit", kwargs={"pk": form.instance.pk}))

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-group-list")
    

    
class AdminProductGroupEditView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, UpdateView):
    template_name = "dashboard/admin/product-group/product-group-edit.html"
    queryset = ProductCategoryModel.objects.all()
    form_class = ProductGroupForm
    success_message = "ویرایش گروه محصول با موفقیت انجام شد"

    def get_success_url(self):
        return reverse_lazy("dashboard:admin:product-group-edit", kwargs={"pk": self.get_object().pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj
    
class AdminProductDeleteView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, DeleteView):
    template_name = "dashboard/admin/product-group/product-group-delete.html"
    queryset = ProductCategoryModel.objects.all()
    success_url = reverse_lazy("dashboard:admin:product-group-list")
    success_message = "حذف گروه محصول با موفقیت انجام شد"