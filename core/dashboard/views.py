from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from django.urls import reverse_lazy
from accounts.models import UserType
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class DashboardHomeView(LoginRequiredMixin, View):
    login_url = reverse_lazy('accounts:login')

    def get(self, request, *args, **kwargs):
        # بررسی اینکه آیا کاربر احراز هویت شده است یا خیر
        if request.user.is_authenticated:
            user_type = request.user.type
            if user_type == UserType.customer.value:
                return redirect(reverse_lazy('dashboard:customer:home'))
            elif user_type == UserType.admin.value:
                return redirect(reverse_lazy('dashboard:admin:home'))
            elif user_type == UserType.superuser.value:
                return redirect(reverse_lazy('dashboard:admin:home'))
            else:
                # اگر نوع کاربر نه مشتری باشد و نه ادمین، به صفحه‌ای مناسب هدایت شود
                return redirect(reverse_lazy('accounts:login'))
        else:
            return redirect(self.login_url)
        

