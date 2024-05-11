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