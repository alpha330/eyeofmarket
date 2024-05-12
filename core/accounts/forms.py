from django.contrib.auth import forms as auth_form
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django import forms
# FORMS TO MANAGE SOME VIEWS AND ACT OF USERS IN accounts APP accounts.forms<---->accounts.views

User=get_user_model()

class AuthenticationForm(auth_form.AuthenticationForm):

    def confirm_login_allowed(self, user):
        super(AuthenticationForm, self).confirm_login_allowed(user)
        if not user.is_verified:
            raise ValidationError("user not verified")


class ResetLinkEmailPassword(forms.Form):
    email = forms.EmailField(required=True)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user_obj = get_object_or_404(User,email=email)
        except User.DoesNotExist:
            raise forms.ValidationError('ایمیل موجود نیست')
        return email
    
class PasswordResetForm(forms.Form):
    
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
    
    def clean(self):
        new_password = super().clean()
        password = new_password.get("password")
        password1 = new_password.get("password1")

        if password and password1 and password != password1:
            raise forms.ValidationError("رمز عبور عبور و تکرار رمز عبور یکسان نیست")
        
        return new_password