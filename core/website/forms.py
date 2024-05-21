from django import forms
from website.models import TicketingFormModel

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