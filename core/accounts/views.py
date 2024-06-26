from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, HttpResponse, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import View,FormView
from django.contrib.auth import views as auth_views
from accounts.forms import AuthenticationForm, ResetLinkEmailPasswordForm, PasswordResetForm , UserRegistrationForm
from django.core.exceptions import ValidationError
import jwt
from django.contrib import messages
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from django.conf import settings
from accounts.tasks import sendEmail
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        response = super().form_valid(form)
        return response

class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("accounts:login")
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)
            sendEmail.delay(
                template="email/activate_user.tpl",
                context={"token": token, "user": str(
                    user_obj)},
                from_email="xigma@afarineshvc.ir",
                recipient_list=[email,],
            )
            
            # You can optionally log in the user after registration
            # login(request, user)
            return redirect('accounts:login')  # Redirect to login page after successful registration
        return render(request, 'accounting/register.html', {'form': form})
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def get_success_url(self):
        messages.success(self.request,"ثبت نام انجام شد  و لینک وریفای ارسال  شد")
        return super().get_success_url()
    
    
class LogoutView(auth_views.LogoutView):
    pass


class ForgetPasswordLinkView(FormView):
    template_name = 'accounts/forget-password.html'
    form_class = ResetLinkEmailPasswordForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = get_object_or_404(User, email=email)

        token = self.get_tokens_for_user(user)
        sendEmail.delay(
                template="email/reset-password.tpl",
                context={"token": token, "user": str(
                    user)},
                from_email="xigma@afarineshvc.ir",
                recipient_list=[email,],
            )

        messages.success(self.request, "ایمیل بازیابی رمز عبور ارسال شد")
        return super().form_valid(form)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)



class ResetPasswordView(FormView):
   template_name = 'accounts/reset-password.html'
   form_class = PasswordResetForm
   success_url = reverse_lazy('accounts:login')
            
   def get_user_from_token(self):
       token = self.kwargs['token']
       try:
           token_data = jwt.decode(
           token, settings.SECRET_KEY, algorithms=["HS256"])
           user_id = token_data.get("user_id")
           return User.objects.get(pk=user_id)
       except (ValueError, User.DoesNotExist):
           return None      
       
   def form_valid(self, form):
       user = self.get_user_from_token()
       if user is None:
            messages.error(self.request, "توکن ریست رمز منقضی شده است")
            return self.form_invalid(form)
       new_password = form.cleaned_data["password"]
       user.set_password(new_password)
       user.save()      
       messages.success(self.request, "رمز شما با موفقیت تغییر یافت")
       return super().form_valid(form)

class ActivateAccountView(View):
    model = User
    
    def get(self, request, token, *args, **kwargs):
        token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = token.get("user_id")
        user_object = User.objects.get(pk=user_id)
        if user_object.is_active == False:
            user_object.is_active = True
            user_object.is_verify = True
            user_object.save()
            messages.success(self.request,"کاربر  فعال شد ")
            return redirect("accounts:login")
        else :
            messages.warning(self.request,"کاربر قبلا فعال شده است")
            return redirect("accounts:login")