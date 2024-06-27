from django import forms
from website.models import TicketingFormModel,NewsLetterModel
from django_recaptcha.widgets import ReCaptchaV2Checkbox,ReCaptchaV3
from django_recaptcha.fields import ReCaptchaField
from django.conf import settings

class TicketForm(forms.ModelForm):
    
    captcha = ReCaptchaField(public_key=settings.GOOGLE_RECAPTCHA_SITE_KEY,
                             private_key=settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                                widget=ReCaptchaV3(
                                    attrs={
                                        'required_score':0.85,
                                    }
                                ),
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