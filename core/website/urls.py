from django.urls import path, include
from website import views
# FROM WEBSITE URLS CONFIG core.urls<---->webiste.urs

app_name = "website"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("news-letter/register/",views.NewsLetterView.as_view(),name="news-letter")
]
