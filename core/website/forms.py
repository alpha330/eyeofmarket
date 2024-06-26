from django import forms
from website.models import TicketingFormModel,NewsLetterModel
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django_recaptcha.fields import ReCaptchaField

class TicketForm(forms.ModelForm):
    
    captcha = ReCaptchaField(
        public_key="6LcLzgEqAAAAAEBMBYp9VmWnP4UCqVlbnGxMmeBP",
        private_key="6LcLzgEqAAAAAFBGfbQzPBeM21rM8sPJvKQ26-cx",
        widget=ReCaptchaV2Checkbox,
        required=True,
        )
    
    class Meta:
        model = TicketingFormModel
        fields = [
            'first_name',
            'last_name',
            'email_address',
            'mobile_number',
            'subject',
            'message',
            'captcha',       
        ]
        
class NewsLetterForm(forms.ModelForm):
    
    class Meta:
        model = NewsLetterModel
        fields = [
            "email",
        ]