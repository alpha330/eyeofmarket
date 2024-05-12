from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import View
from django.contrib.auth import views as auth_views
from accounts.forms import AuthenticationForm, ResetLinkEmailPassword, PasswordResetForm
from django.core.exceptions import ValidationError
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from django.conf import settings
from accounts.tasks import sendEmail
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from accounts.models import Profile
# Create your views here.

User = get_user_model()


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    pass


class ForgetPasswordLinkView(View):
    template_name = 'accounts/forget-password.html'

    def get(self, request):
        form = ResetLinkEmailPassword()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ResetLinkEmailPassword(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)
            profile = Profile.objects.get(user=user_obj)
            sendEmail.delay(
                template="email/reset-password.tpl",
                context={"token": token, "user": str(
                    user_obj), "profile": str(profile), },
                from_email="xigma@afarineshvc.ir",
                recipient_list=[email,],
            )
            request.session["message"] = "ایمیل بازیابی رمز عبور ارسال شد"
            return HttpResponseRedirect(reverse_lazy('accounts:login'))
        return render(request, self.template_name, {'form': form})
        # You can optionally log in the user after registration
        # login(request, user)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ResetPasswordView(View):
    template_name = 'accounts/reset-password.html'
    form_class = PasswordResetForm

    def get(self, request, token, *args, **kwargs):
        try:
            token_data = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token_data.get("user_id")
        except ExpiredSignatureError:
            raise ValidationError (" توکن منقضی شده است")
        except InvalidSignatureError:
            raise ValidationError("توکن نا معتبر است")

        user = User.objects.get(pk=user_id)
        form = self.form_class()
        return render(request, self.template_name, {'token': token, 'user': user, 'form': form})

    def post(self, request, token, *args, **kwargs):
        try:
            token_data = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token_data.get("user_id")
        except ExpiredSignatureError:
            raise ValidationError (" توکن منقضی شده است")
        except InvalidSignatureError:
            raise ValidationError("توکن نا معتبر است")

        user = User.objects.get(pk=user_id)
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data["password"]
            user.set_password(new_password)
            user.save()
            request.session["message"] = "رمز شما با موفقیت تغییر یافت"
            return redirect('accounts:login')
        else:
            return HttpResponseRedirect(reverse("accounts:reset-password", kwargs={'token': token}))
