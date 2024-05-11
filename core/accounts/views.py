from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth import views as auth_views
from accounts.forms import AuthenticationForm,ResetLinkEmailPassword
from accounts.tasks import sendEmail
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from accounts.models import Profile
# Create your views here.

User=get_user_model()
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
            profile=Profile.objects.get(user=user_obj)
            sendEmail.delay(                
                template="email/reset-password.tpl",
                context={"token":token,"user":str(user_obj),"profile":str(profile),},
                from_email="xigma@afarineshvc.ir",
                recipient_list=[email,],          
            )        
            request.session["message"]="ایمیل بازیابی رمز عبور ارسال شد"
            return HttpResponseRedirect(reverse_lazy('accounts:login'))
        return render(request, self.template_name, {'form': form})
        # You can optionally log in the user after registration
        # login(request, user)
        
    
    
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)