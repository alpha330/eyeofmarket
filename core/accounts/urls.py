from django.urls import path, include
from accounts import views
# FROM WEBSITE URLS CONFIG core.urls<---->webiste.urs

app_name = "accounts"

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='login'),
    # path('register/',views.LoginView.as_view(),name='register'),
    path('forget/password/',views.ForgetPasswordLinkView.as_view(),name='forget'),
    path('reset/<str:token>/password/',views.ResetPasswordView.as_view(),name='reset-password'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
]
