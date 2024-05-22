from django.db import models
from website.validators import validate_iranian_cellphone_number
# Create your models here.

class TicketingFormModel(models.Model):
    first_name = models.CharField(max_length=255,help_text="نام")
    last_name = models.CharField(max_length=255,help_text="نام خانوادگی")
    email_address = models.EmailField(help_text="ادرس ایمیل")
    mobile_number = models.CharField(max_length=11,validators=[validate_iranian_cellphone_number],help_text="شماره موبایل")
    subject = models.CharField(max_length=255,help_text="موضوع")
    message = models.TextField(help_text="پیغام")
    created_at = models.DateTimeField(auto_now=True,help_text="تاریخ تولید پیغام")
    
    def __str__(self):
        
        return self.email_address
    
class NewsLetterModel(models.Model):
    email = models.EmailField(help_text="ایمیل عضویت در خبر نامه")
    created_at = models.DateTimeField(auto_now=True,help_text="تاریخ  عضویت")
    
    def __str__(self):
        return self.email