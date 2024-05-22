from django import forms
from website.models import TicketingFormModel,NewsLetterModel

class TicketForm(forms.ModelForm):
    
    class Meta:
        model = TicketingFormModel
        fields = [
            'first_name',
            'last_name',
            'email_address',
            'mobile_number',
            'subject',
            'message',       
        ]
        
class NewsLetterForm(forms.ModelForm):
    
    class Meta:
        model = NewsLetterModel
        fields = [
            "email",
        ]