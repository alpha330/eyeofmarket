from django.contrib.auth import forms as auth_form
from django.core.exceptions import ValidationError

# FORMS TO MANAGE SOME VIEWS AND ACT OF USERS IN accounts APP accounts.forms<---->accounts.views


class AuthenticationForm(auth_form.AuthenticationForm):

    def confirm_login_allowed(self, user):
        super(AuthenticationForm, self).confirm_login_allowed(user)
        if not user.is_verified:
            raise ValidationError("user not verified")
