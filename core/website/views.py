from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView,FormView
from django.urls import reverse
from django.contrib import messages
from website.forms import TicketForm
from accounts.tasks import sendEmail
# VIEWS CONFIG OF WEBSITE APP webiste.urls <----> website.views


class IndexView(TemplateView):
    template_name = "website/index.html"


class ContactView(FormView):
    template_name = "website/contact.html"
    form_class = TicketForm
    
    def form_valid(self, form):
        email = form.cleaned_data["email_address"]
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        sendEmail.delay(
            template="email/contact_us.tpl",
            context={"email": email, "first_name": first_name,"last_name":last_name},
            from_email="xigma@afarineshvc.ir",
            recipient_list=[email,],
        )
        messages.success(self.request, "درخواست شما ثبت شد")
        form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('website:index')


class AboutView(TemplateView):
    template_name = "website/about.html"

