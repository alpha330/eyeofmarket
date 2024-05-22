from django.contrib import admin
from website.models import TicketingFormModel, NewsLetterModel
# Register your models here.

class TicketingFormAdminModel(admin.ModelAdmin):
    
    model = TicketingFormModel
    list_display = ('first_name','last_name','email_address','mobile_number','subject','created_at')
    search_fields = ('first_name', 'last_name', 'email_address', 'mobile_number')
    
class NewsLetterAdmin(admin.ModelAdmin):
    
    model = NewsLetterModel
    list_display = ('email', 'created_at')
    
admin.site.register(TicketingFormModel,TicketingFormAdminModel)
admin.site.register(NewsLetterModel,NewsLetterAdmin)