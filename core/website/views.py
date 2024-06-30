from django.views.generic import TemplateView, FormView
from django.urls import reverse
from django.contrib import messages
from website.forms import TicketForm, NewsLetterForm
from accounts.tasks import sendEmail
from accounts.models import Profile
from shop.models import ProductModel,ProductCategoryModel
from django.db.models import Count
# VIEWS CONFIG OF WEBSITE APP webiste.urls <----> website.views


class IndexView(TemplateView):
    template_name = "website/index.html"
    
    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        selected_products = ProductModel.objects.filter(status=1, is_featured=True)[:3]
        prime_group = ProductCategoryModel.objects.filter(is_featured=True)[:3]
        if selected_products :
            context["select_1"]=selected_products[0]
            context["select_2"]=selected_products[1]
            context["select_3"]=selected_products[2]
        else:
            print("No Product in Stock")
            messages.warning(self.request,"محصولی در انبار موجود نیست")
            
        if len(prime_group) == 3:
            card_a = ProductModel.objects.filter(status=1,category=prime_group[0])[:3]
            context["card_a_1"]=card_a[0]
            context["card_a_2"]=card_a[1]
            context["card_a_3"]=card_a[2]
        else:
            print("No Product in Stock")
            messages.warning(self.request,"محصولی در گروه محصول موجود نیست")
          
        return context
            
    
    


class ContactView(FormView):
    template_name = "website/contact.html"
    form_class = TicketForm

    def form_valid(self, form):
        email = form.cleaned_data["email_address"]
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        sendEmail.delay(
            template="email/contact_us.tpl",
            context={"email": email, "first_name": first_name,
                     "last_name": last_name},
            from_email="xigma@afarineshvc.ir",
            recipient_list=[email,],
        )
        messages.success(self.request, "درخواست شما ثبت شد")
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super(ContactView, self).get_context_data(**kwargs)
            user = self.request.user
            context["profile"] = Profile.objects.get(user=user)
            return context
        else:
            pass

    def get_success_url(self):
        return reverse('website:index')

class NewsLetterView(FormView):
    form_class = NewsLetterForm
    template_name = "include/news-letter.html"
    
    def form_valid(self, form):
        email = form.cleaned_data["email"]
        sendEmail.delay(
            template="email/newsletter_register.tpl",
            context={"email": email},
            from_email="xigma@afarineshvc.ir",
            recipient_list=[email,],
        )
        messages.success(self.request, "ایمیل سما با موفقیت در خبر نامه ثبت شد")
        form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('website:index')
    

class AboutView(TemplateView):
    template_name = "website/about.html"
