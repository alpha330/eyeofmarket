from django.contrib.auth import forms as auth_form
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms
import re
# FORMS TO MANAGE SOME VIEWS AND ACT OF USERS IN accounts APP accounts.forms<---->accounts.views

User = get_user_model()


class AuthenticationForm(auth_form.AuthenticationForm):

    def confirm_login_allowed(self, user):
        super(AuthenticationForm, self).confirm_login_allowed(user)
        if not user.is_verified:
            raise ValidationError(_("کاربر وریفای نشده است"))


class ResetLinkEmailPasswordForm(forms.Form):
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(_('ایمیل موجود نیست'))

        if not user_obj.is_active:
            raise forms.ValidationError(_('حساب کاربری غیرفعال است'))

        return email


class PasswordResetForm(forms.Form):
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        min_length=8,
        help_text=_('Minimum 8 characters.'),
    )
    password1 = forms.CharField(
        label=_('Repeat Password'),
        widget=forms.PasswordInput,
    )

    def clean_password1(self):
        password = self.cleaned_data.get('password')
        if password is None or len(password) < 8:
            raise forms.ValidationError(
                _('رمز عبور باید حداقل 8 کاراکتر داشته باشد.'))
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError(
                _('رمز عبور باید حداقل یک حرف بزرگ داشته باشد.'))
        
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError(
                _('رمز عبور باید حداقل یک حرف کوچک داشته باشد.'))

        if not re.search(r'\d', password):
            raise forms.ValidationError(
                _('رمز عبور باید حداقل یک عدد داشته باشد.'))

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError(
                _('رمز عبور باید حداقل یک علامت ویژه داشته باشد.'))
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                _('رمز عبور عبور و تکرار رمز عبور یکسان نیست.'))

        return password2
