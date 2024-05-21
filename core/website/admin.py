from django.contrib import admin
from website.models import TicketingFormModel
# Register your models here.

class TicketingFormAdminModel(admin.ModelAdmin):
    
    model = TicketingFormModel
    list_display = ('first_name','last_name','email_address','mobile_number','subject','created_at')
    search_fields = ('first_name', 'last_name', 'email_address', 'mobile_number')
    
admin.site.register(TicketingFormModel,TicketingFormAdminModel)