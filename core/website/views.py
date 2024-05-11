from django.shortcuts import render
from django.views.generic import TemplateView

# VIEWS CONFIG OF WEBSITE APP webiste.urls <----> website.views


class IndexView(TemplateView):
    template_name = "website/index.html"


class ContactView(TemplateView):
    template_name = "website/contact.html"


class AboutView(TemplateView):
    template_name = "website/about.html"
