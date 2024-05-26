from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from accounts.models import UserType
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions import HasAdminAccessPermission
from dashboard.admin.forms import *
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import views as auth_views
# Create your views here.


class AdminDashboardHomeView(LoginRequiredMixin, HasAdminAccessPermission, TemplateView):
    template_name = "dashboard/admin/home.html"

class AdminSecurityEditView(LoginRequiredMixin, HasAdminAccessPermission,SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = "dashboard/admin/profile/security-edit.html"
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy("dashboard:admin:security-edit")
    success_message = "بروز رسانی پسورد با موفقیت انجام شد"